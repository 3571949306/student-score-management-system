package com.example.securitydemo.controller;

import com.example.securitydemo.entity.SysRole;
import com.example.securitydemo.entity.SysUser;
import com.example.securitydemo.repository.SysRoleRepository;
import com.example.securitydemo.repository.SysUserRepository;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.security.core.Authentication;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/admin/users")
public class AdminUserController {

    private final SysUserRepository userRepository;
    private final SysRoleRepository roleRepository;
    private final PasswordEncoder passwordEncoder;

    public AdminUserController(SysUserRepository userRepository, SysRoleRepository roleRepository, PasswordEncoder passwordEncoder) {
        this.userRepository = userRepository;
        this.roleRepository = roleRepository;
        this.passwordEncoder = passwordEncoder;
    }

    @GetMapping
    public String list(Authentication authentication, Model model) {
        addModel(authentication, model, new AccountForm());
        return "admin-users";
    }

    @PostMapping
    public String create(@ModelAttribute AccountForm form) {
        SysUser user = new SysUser();
        user.setUsername(form.getUsername());
        user.setPassword(passwordEncoder.encode(form.getPassword()));
        user.setEnabled(Boolean.TRUE.equals(form.getEnabled()));
        if (form.getRoleId() != null) {
            SysRole role = roleRepository.findById(form.getRoleId()).orElse(null);
            if (role != null) {
                user.addRole(role);
            }
        }
        userRepository.save(user);
        return "redirect:/admin/users";
    }

    @GetMapping("/{id}/edit")
    public String edit(@PathVariable Long id, Authentication authentication, Model model) {
        SysUser user = userRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("账号不存在：" + id));
        AccountForm form = new AccountForm();
        form.setId(user.getId());
        form.setUsername(user.getUsername());
        form.setPassword("");
        form.setEnabled(user.getEnabled());
        user.getRoles().stream().findFirst().map(SysRole::getId).ifPresent(form::setRoleId);
        addModel(authentication, model, form);
        return "admin-users";
    }

    @PostMapping("/{id}")
    public String update(@PathVariable Long id, @ModelAttribute AccountForm form) {
        SysUser user = userRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("账号不存在：" + id));
        user.setUsername(form.getUsername());
        if (form.getPassword() != null && !form.getPassword().isEmpty()) {
            user.setPassword(passwordEncoder.encode(form.getPassword()));
        }
        user.setEnabled(Boolean.TRUE.equals(form.getEnabled()));
        user.clearRoles();
        if (form.getRoleId() != null) {
            SysRole role = roleRepository.findById(form.getRoleId()).orElse(null);
            if (role != null) {
                user.addRole(role);
            }
        }
        userRepository.save(user);
        return "redirect:/admin/users";
    }

    @PostMapping("/{id}/delete")
    public String delete(@PathVariable Long id, Authentication authentication) {
        SysUser user = userRepository.findById(id)
                .orElseThrow(() -> new IllegalArgumentException("账号不存在：" + id));
        if (!authentication.getName().equals(user.getUsername())) {
            userRepository.delete(user);
        }
        return "redirect:/admin/users";
    }

    private void addModel(Authentication authentication, Model model, AccountForm form) {
        if (form.getRoleId() == null) {
            roleRepository.findByName("ROLE_STUDENT").map(SysRole::getId).ifPresent(form::setRoleId);
        }
        List<AccountRow> users = userRepository.findAll().stream()
                .map(user -> new AccountRow(user))
                .collect(Collectors.toList());
        model.addAttribute("users", users);
        model.addAttribute("roles", roleRepository.findAll());
        model.addAttribute("accountForm", form);
        model.addAttribute("username", authentication.getName());
        model.addAttribute("formAction", form.getId() == null ? "/admin/users" : "/admin/users/" + form.getId());
    }

    public static class AccountRow {
        private final SysUser user;
        private final String roleText;

        public AccountRow(SysUser user) {
            this.user = user;
            this.roleText = user.getRoles().stream()
                    .map(SysRole::getDescription)
                    .collect(Collectors.joining(", "));
        }

        public SysUser getUser() {
            return user;
        }

        public String getRoleText() {
            return roleText;
        }
    }

    public static class AccountForm {
        private Long id;
        private String username;
        private String password = "123";
        private Boolean enabled = true;
        private Long roleId;

        public Long getId() {
            return id;
        }

        public void setId(Long id) {
            this.id = id;
        }

        public String getUsername() {
            return username;
        }

        public void setUsername(String username) {
            this.username = username;
        }

        public String getPassword() {
            return password;
        }

        public void setPassword(String password) {
            this.password = password;
        }

        public Boolean getEnabled() {
            return enabled;
        }

        public void setEnabled(Boolean enabled) {
            this.enabled = enabled;
        }

        public Long getRoleId() {
            return roleId;
        }

        public void setRoleId(Long roleId) {
            this.roleId = roleId;
        }
    }
}
