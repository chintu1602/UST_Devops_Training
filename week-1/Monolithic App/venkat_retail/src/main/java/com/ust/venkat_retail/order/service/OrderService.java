package com.ust.venkat_retail.order.service;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;
import com.ust.venkat_retail.order.entity.Order;
import com.ust.venkat_retail.order.repository.OrderRepository;
import com.ust.venkat_retail.product.service.ProductService;
import com.ust.venkat_retail.product.entity.Product;

@Service
@RequiredArgsConstructor
public class OrderService {

    private final OrderRepository repo;
    private final ProductService productService;

    public Order create(Long productId, int qty){

        Product p = productService.get(productId);

        if(p.getQuantity() < qty)
            throw new RuntimeException("Not enough stock");

        p.setQuantity(p.getQuantity()-qty);
        productService.add(p);

        Order o = new Order();
        o.setProductId(productId);
        o.setQuantity(qty);
        o.setTotalPrice(p.getPrice()*qty);

        return repo.save(o);
    }

    public List<Order> getAll(){
        return repo.findAll();
    }
}