package com.example.securitydemo.service;

import com.example.securitydemo.entity.StudentScore;
import com.example.securitydemo.repository.StudentScoreRepository;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import org.springframework.stereotype.Service;
import weka.classifiers.trees.RandomForest;
import weka.core.Attribute;
import weka.core.DenseInstance;
import weka.core.Instances;

@Service
public class ScorePredictionService {

    private final StudentScoreRepository scoreRepository;
    private boolean trained = false;
    private final Map<String, Map<String, Integer>> categoricalIndexes = new HashMap<>();
    private int trainingCount = 0;

    // Grade level boundaries for classification
    private static final String[] GRADE_LEVELS = {"不及格", "及格", "中等", "良好", "优秀"};
    private static final double[] GRADE_BOUNDARIES = {60, 90, 110, 130};

    public ScorePredictionService(StudentScoreRepository scoreRepository) {
        this.scoreRepository = scoreRepository;
    }

    private static String scoreToLevel(double score) {
        if (score >= 130) return "优秀";
        if (score >= 110) return "良好";
        if (score >= 90) return "中等";
        if (score >= 60) return "及格";
        return "不及格";
    }

    public synchronized Instances trainModel(String studentName) {
        if (trained) {
            return null;
        }

        List<StudentScore> scores;
        if (studentName != null && !studentName.isEmpty()) {
            scores = scoreRepository.findByStudentNameOrderByStudentNumberAsc(studentName);
        } else {
            scores = scoreRepository.findAll();
        }

        if (scores.isEmpty()) {
            return null;
        }

        trainingCount = scores.size();

        Map<String, List<String>> categoricalValues = new HashMap<>();
        for (StudentScore s : scores) {
            addValues(categoricalValues, "studentName", s.getStudentName());
            addValues(categoricalValues, "studentNumber", s.getStudentNumber());
            addValues(categoricalValues, "subject", s.getSubject());
            addValues(categoricalValues, "examName", s.getExamName());
            addValues(categoricalValues, "semester", s.getSemester());
        }

        // Remove duplicate values before creating Weka attributes
        for (List<String> vals : categoricalValues.values()) {
            List<String> distinct = new ArrayList<>(new java.util.LinkedHashSet<>(vals));
            vals.clear();
            vals.addAll(distinct);
        }

        List<String> attributes = Arrays.asList("studentName", "studentNumber", "subject", "examName", "semester");
        List<Attribute> attrList = new ArrayList<>();
        for (String attrName : attributes) {
            List<String> vals = categoricalValues.get(attrName);
            Collections.sort(vals);
            attrList.add(new Attribute(attrName, vals));
        }
        // Class attribute: grade level (nominal)
        attrList.add(new Attribute("gradeLevel", Arrays.asList(GRADE_LEVELS)));
        Instances data = new Instances("ScoreData", new ArrayList<>(attrList), scores.size());
        data.setClassIndex(data.numAttributes() - 1);

        for (StudentScore s : scores) {
            double[] values = new double[data.numAttributes()];
            for (int i = 0; i < attributes.size(); i++) {
                Attribute attr = data.attribute(attributes.get(i));
                String val = getAttrValue(s, attributes.get(i));
                values[i] = attr.indexOfValue(val);
            }
            // Set class value as grade level
            String level = scoreToLevel(s.getScore().doubleValue());
            values[data.numAttributes() - 1] = data.attribute("gradeLevel").indexOfValue(level);
            data.add(new DenseInstance(1.0, values));
        }

        categoricalIndexes.clear();
        for (String attrName : attributes) {
            Attribute attr = data.attribute(attrName);
            Map<String, Integer> map = new HashMap<>();
            for (int i = 0; i < attr.numValues(); i++) {
                map.put(attr.value(i), i);
            }
            categoricalIndexes.put(attrName, map);
        }
        // Store grade level index map
        Attribute gradeAttr = data.attribute("gradeLevel");
        Map<String, Integer> gradeMap = new HashMap<>();
        for (int i = 0; i < gradeAttr.numValues(); i++) {
            gradeMap.put(gradeAttr.value(i), i);
        }
        categoricalIndexes.put("gradeLevel", gradeMap);

        try {
            RandomForest rf = new RandomForest();
            rf.buildClassifier(data);
            trained = true;
            return data;
        } catch (Exception e) {
            throw new RuntimeException("训练失败", e);
        }
    }

    public synchronized Map<String, Object> predict(String studentName, String studentNumber,
            String subject, String examName, String semester) throws Exception {
        if (!trained) {
            throw new IllegalStateException("模型尚未训练，请先训练模型");
        }

        List<String> attributes = Arrays.asList("studentName", "studentNumber", "subject", "examName", "semester");
        List<Attribute> attrList = new ArrayList<>();
        for (String attrName : attributes) {
            Map<String, Integer> idxMap = categoricalIndexes.get(attrName);
            if (idxMap == null) {
                throw new IllegalArgumentException("未知的分类属性：" + attrName);
            }
            List<String> vals = new ArrayList<>(idxMap.keySet());
            Collections.sort(vals);
            attrList.add(new Attribute(attrName, vals));
        }
        // Class attribute: grade level
        attrList.add(new Attribute("gradeLevel", Arrays.asList(GRADE_LEVELS)));
        Instances data = new Instances("ScoreData", new ArrayList<>(attrList), 1);
        data.setClassIndex(data.numAttributes() - 1);

        double[] values = new double[data.numAttributes()];
        for (int i = 0; i < attributes.size(); i++) {
            Attribute attr = data.attribute(attributes.get(i));
            String val = null;
            switch (attributes.get(i)) {
                case "studentName": val = studentName; break;
                case "studentNumber": val = studentNumber; break;
                case "subject": val = subject; break;
                case "examName": val = examName; break;
                case "semester": val = semester; break;
            }
            if (val == null || !idxMapContains(attributes.get(i), val)) {
                throw new IllegalArgumentException("属性值不在训练集中：" + attributes.get(i) + "=" + val);
            }
            values[i] = attr.indexOfValue(val);
        }
        values[data.numAttributes() - 1] = 0;
        data.add(new DenseInstance(1.0, values));

        RandomForest rf = new RandomForest();
        rf.buildClassifier(data);
        double predictedIndex = rf.classifyInstance(data.instance(0));
        double[] dist = rf.distributionForInstance(data.instance(0));
        double confidence = 0;
        for (double p : dist) {
            confidence = Math.max(confidence, p);
        }

        // Get predicted grade level
        String level = GRADE_LEVELS[(int) predictedIndex];

        // Calculate approximate score from grade level (midpoint of range)
        double approxScore;
        switch (level) {
            case "优秀": approxScore = 140; break;
            case "良好": approxScore = 120; break;
            case "中等": approxScore = 100; break;
            case "及格": approxScore = 75; break;
            default: approxScore = 45; break;
        }

        Map<String, Object> result = new HashMap<>();
        result.put("studentName", studentName);
        result.put("studentNumber", studentNumber);
        result.put("subject", subject);
        result.put("examName", examName);
        result.put("semester", semester);
        result.put("predictedScore", approxScore);
        result.put("confidence", Math.round(confidence * 10000.0) / 100.0);
        result.put("level", level);
        result.put("modelInfo", "随机森林 (训练样本数：" + trainingCount + ")");
        return result;
    }

    public boolean isTrained() { return trained; }

    public int getTrainingCount() { return trainingCount; }

    private boolean idxMapContains(String attrName, String value) {
        Map<String, Integer> map = categoricalIndexes.get(attrName);
        return map != null && map.containsKey(value);
    }

    private String getAttrValue(StudentScore s, String attr) {
        switch (attr) {
            case "studentName": return s.getStudentName();
            case "studentNumber": return s.getStudentNumber();
            case "subject": return s.getSubject();
            case "examName": return s.getExamName();
            case "semester": return s.getSemester();
            default: return "";
        }
    }

    private void addValues(Map<String, List<String>> map, String key, String value) {
        map.computeIfAbsent(key, k -> new ArrayList<>()).add(value);
    }
}
