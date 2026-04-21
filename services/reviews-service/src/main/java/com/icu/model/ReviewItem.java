package com.icu.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import com.fasterxml.jackson.annotation.JsonProperty;

@Entity
@Table(name = "review_item")
public class ReviewItem {
    
    @Id
    @JsonProperty("review_item_id")
    private Integer reviewItemId;
    
    @JsonProperty("review_id")
    private Integer reviewId;
    
    @JsonProperty("item_id")
    private Integer itemId;
    
    private Integer quantity;

    // Constructors
    public ReviewItem() {}

    public ReviewItem(Integer reviewItemId, Integer reviewId, Integer itemId, Integer quantity) {
        this.reviewItemId = reviewItemId;
        this.reviewId = reviewId;
        this.itemId = itemId;
        this.quantity = quantity;
    }

    // Getters and Setters
    public Integer getReviewItemId() {
        return reviewItemId;
    }

    public void setReviewItemId(Integer reviewItemId) {
        this.reviewItemId = reviewItemId;
    }

    public Integer getReviewId() {
        return reviewId;
    }

    public void setReviewId(Integer reviewId) {
        this.reviewId = reviewId;
    }

    public Integer getItemId() {
        return itemId;
    }

    public void setItemId(Integer itemId) {
        this.itemId = itemId;
    }

    public Integer getQuantity() {
        return quantity;
    }

    public void setQuantity(Integer quantity) {
        this.quantity = quantity;
    }
}
