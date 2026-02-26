package com.ust.venkat_retail.product.controller;

import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;
import java.util.List;
import com.ust.venkat_retail.product.entity.Product;
import com.ust.venkat_retail.product.service.ProductService;

@RestController
@RequestMapping("/products")
@RequiredArgsConstructor
public class ProductController {

    private final ProductService service;

    @PostMapping
    public Product add(@RequestBody Product p){
        return service.add(p);
    }

    @GetMapping
    public List<Product> getAll(){
        return service.getAll();
    }

    @GetMapping("/{id}")
    public Product get(@PathVariable Long id){
        return service.get(id);
    }
}