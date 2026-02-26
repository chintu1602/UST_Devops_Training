package com.UST.retails.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import com.UST.retails.repository.OrderRepository;
import com.UST.retails.entity.Order;

import java.util.List;

@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository orderRepository;

    public Order save(Order order) {
        return orderRepository.save(order);
    }

    public List<Order> getAll() {
        return orderRepository.findAll();
    }
}