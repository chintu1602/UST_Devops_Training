package com.UST.retails.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.UST.retails.entity.Order;

public interface OrderRepository extends JpaRepository<Order, Long> {
}