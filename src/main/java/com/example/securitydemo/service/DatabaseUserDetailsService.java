package com.example.securitydemo.service;

import com.example.securitydemo.entity.SysRole;
import com.example.securitydemo.entity.SysUser;
import com.example.securitydemo.repository.SysRoleRepository;
import com.example.securitydemo.repository.SysUserRepository;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
public class DatabaseUserDetailsService implements UserDetailsService {

    private final SysUserRepository userRepository;
    private final SysRoleRepository roleRepository;

    public DatabaseUserDetailsService(SysUserRepository userRepository, SysRoleRepository roleRepository) {
        this.userRepository = userRepository;
        this.roleRepository = roleRepository;
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        SysUser user = userRepository.findByUsername(username)
                .orElseThrow(() -> new UsernameNotFoundException("用户不存在：" + username));
        List<SimpleGrantedAuthority> authorities = roleRepository.findRolesByUsername(username).stream()
                .map(SysRole::getName)
                .map(SimpleGrantedAuthority::new)
                .collect(Collectors.toList());

        return User.builder()
                .username(user.getUsername())
                .password(user.getPassword())
                .disabled(!Boolean.TRUE.equals(user.getEnabled()))
                .authorities(authorities)
                .build();
    }
}
