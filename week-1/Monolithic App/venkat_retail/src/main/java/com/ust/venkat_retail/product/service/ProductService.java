package com.ust.venkat_retail.product.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;
import com.ust.venkat_retail.product.entity.Product;
import com.ust.venkat_retail.product.repository.ProductRepository;

@Service
@RequiredArgsConstructor
public class ProductService {

    private final ProductRepository repo;

    public Product add(Product p){
        return repo.save(p);
    }

    public List<Product> getAll(){
        return repo.findAll();
    }

    public Product get(Long id){
        return repo.findById(id).orElseThrow();
    }
}