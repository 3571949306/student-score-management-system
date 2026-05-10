package com.example.securitydemo.controller;

import com.example.securitydemo.entity.StudentScore;
import com.example.securitydemo.repository.StudentScoreRepository;
import com.example.securitydemo.service.ScorePredictionService;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

@Controller
@RequestMapping("/prediction")
public class PredictionController {

    private final ScorePredictionService predictionService;
    private final StudentScoreRepository scoreRepository;

    public PredictionController(ScorePredictionService predictionService,
            StudentScoreRepository scoreRepository) {
        this.predictionService = predictionService;
        this.scoreRepository = scoreRepository;
    }

    @GetMapping
    public String index(Authentication authentication, Model model) {
        String username = authentication.getName();
        boolean canPredict = canPredict(authentication);
        model.addAttribute("username", username);
        model.addAttribute("canPredict", canPredict);

        if (!canPredict) {
            return handleStudentPrediction(username, model);
        }

        String modelInfo = predictionService.isTrained()
                ? "模型已训练 (训练样本数：" + predictionService.getTrainingCount() + ")"
                : "模型尚未训练，请先点击训练模型";

        model.addAttribute("trained", predictionService.isTrained());
        model.addAttribute("modelInfo", modelInfo);
        return "prediction";
    }

    private String handleStudentPrediction(String username, Model model) {
        List<StudentScore> studentScores = scoreRepository.findByStudentNameOrderBySemesterDescExamDateDesc(username);

        if (!studentScores.isEmpty()) {
            return showPredictionForStudent(username, studentScores, model);
        }

        model.addAttribute("noData", true);
        return "prediction-student";
    }

    private String showPredictionForStudent(String studentName, List<StudentScore> scores, Model model) {
        // Train model with this student's data if not trained
        if (!predictionService.isTrained()) {
            try {
                predictionService.trainModel(studentName);
            } catch (Exception e) {
                model.addAttribute("noData", true);
                return "prediction-student";
            }
        }

        // Auto-predict for the most recent exam
        StudentScore latestScore = scores.get(scores.size() - 1);
        try {
            Map<String, Object> result = predictionService.predict(
                    studentName,
                    latestScore.getStudentNumber(),
                    latestScore.getSubject(),
                    latestScore.getExamName(),
                    latestScore.getSemester()
            );
            model.addAttribute("predictionData", result);
        } catch (Exception e) {
            model.addAttribute("noData", true);
        }
        return "prediction-student";
    }

    @PostMapping("/train")
    public String train(Authentication authentication, RedirectAttributes redirectAttributes) {
        String username = authentication.getName();
        boolean canPredict = canPredict(authentication);
        if (!canPredict) {
            redirectAttributes.addFlashAttribute("error", "无权限执行此操作");
            return "redirect:/prediction";
        }

        try {
            predictionService.trainModel(null);
            redirectAttributes.addFlashAttribute("message", "模型训练成功！");
        } catch (Exception e) {
            redirectAttributes.addFlashAttribute("error", "模型训练失败：" + e.getMessage());
        }
        return "redirect:/prediction";
    }

    @PostMapping("/predict")
    public String predict(Authentication authentication,
            @RequestParam String studentName,
            @RequestParam String studentNumber,
            @RequestParam String subject,
            @RequestParam String examName,
            @RequestParam String semester,
            Model model,
            RedirectAttributes redirectAttributes) {
        String username = authentication.getName();
        model.addAttribute("username", username);

        try {
            Map<String, Object> result = predictionService.predict(studentName, studentNumber, subject, examName, semester);
            model.addAttribute("prediction", result);
        } catch (Exception e) {
            redirectAttributes.addFlashAttribute("error", "预测失败：" + e.getMessage());
            return "redirect:/prediction";
        }

        String modelInfo = predictionService.isTrained()
                ? "模型已训练 (训练样本数：" + predictionService.getTrainingCount() + ")"
                : "模型尚未训练，请先点击训练模型";

        model.addAttribute("trained", predictionService.isTrained());
        model.addAttribute("modelInfo", modelInfo);
        return "prediction";
    }

    private boolean canPredict(Authentication authentication) {
        return authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .anyMatch(role -> "ROLE_TEACHER".equals(role) || "ROLE_ADMIN".equals(role));
    }
}
