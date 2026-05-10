package com.example.securitydemo.repository;

import com.example.securitydemo.entity.SysRole;
import java.util.List;
import java.util.Optional;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

public interface SysRoleRepository extends JpaRepository<SysRole, Long> {

    Optional<SysRole> findByName(String name);

    @Query("select r from SysUser u join u.roles r where u.username = :username order by r.id")
    List<SysRole> findRolesByUsername(@Param("username") String username);
}
