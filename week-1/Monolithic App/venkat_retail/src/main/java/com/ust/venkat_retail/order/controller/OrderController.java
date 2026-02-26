package com.ust.venkat_retail.order.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import com.ust.venkat_retail.order.entity.Order;
import com.ust.venkat_retail.order.service.OrderService;

@RestController
@RequestMapping("/orders")
@RequiredArgsConstructor
public class OrderController {

    private final OrderService service;

    @PostMapping
    public Order create(@RequestParam Long productId,
                        @RequestParam int quantity){
        return service.create(productId, quantity);
    }

    @GetMapping
    public List<Order> getAll(){
        return service.getAll();
    }
}