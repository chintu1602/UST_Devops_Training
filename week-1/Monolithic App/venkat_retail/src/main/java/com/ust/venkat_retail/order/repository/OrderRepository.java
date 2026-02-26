package com.ust.venkat_retail.order.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.ust.venkat_retail.order.entity.Order;

public interface OrderRepository extends JpaRepository<Order, Long> {}