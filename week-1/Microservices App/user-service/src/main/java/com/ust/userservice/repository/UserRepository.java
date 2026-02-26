package com.ust.userservice.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.ust.userservice.entity.User;

public interface UserRepository extends JpaRepository<User, Long> {
}