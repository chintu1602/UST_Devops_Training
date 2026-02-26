package com.ust.venkat_retail.product.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import com.ust.venkat_retail.product.entity.Product;

public interface ProductRepository extends JpaRepository<Product, Long> {}