package com.example.securitydemo.controller;

import java.security.Principal;
import java.util.stream.Collectors;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class PageController {

    @GetMapping({"/", "/login"})
    public String login() {
        return "login";
    }

    @GetMapping("/user/loginSuccess")
    public String userLoginSuccess(Authentication authentication, Model model) {
        addLoginInfo(authentication, model);
        return "login-success";
    }

    @GetMapping("/admin/main")
    public String adminMain(Authentication authentication, Model model) {
        addLoginInfo(authentication, model);
        return "admin-main";
    }

    @GetMapping("/accessDenied")
    public String accessDenied(Authentication authentication, Principal principal, Model model) {
        String username = principal == null ? "当前用户" : principal.getName();
        model.addAttribute("username", username);
        model.addAttribute("roles", authentication == null ? "" : getRoleText(authentication));
        return "access-denied";
    }

    private void addLoginInfo(Authentication authentication, Model model) {
        model.addAttribute("username", authentication.getName());
        model.addAttribute("roles", getRoleText(authentication));
    }

    private String getRoleText(Authentication authentication) {
        return authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .collect(Collectors.joining(", "));
    }
}
