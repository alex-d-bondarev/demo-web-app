package com.icu.model;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.time.LocalDateTime;

@Entity
@Table(name = "review")
public class Review {
    
    @Id
    @JsonProperty("review_id")
    private Integer reviewId;
    
    @JsonProperty("start_dt")
    private LocalDateTime startDt;
    
    @JsonProperty("end_dt")
    private LocalDateTime endDt;
    
    private String status;

    // Constructors
    public Review() {}

    public Review(Integer reviewId, LocalDateTime startDt, LocalDateTime endDt, String status) {
        this.reviewId = reviewId;
        this.startDt = startDt;
        this.endDt = endDt;
        this.status = status;
    }

    // Getters and Setters
    public Integer getReviewId() {
        return reviewId;
    }

    public void setReviewId(Integer reviewId) {
        this.reviewId = reviewId;
    }

    public LocalDateTime getStartDt() {
        return startDt;
    }

    public void setStartDt(LocalDateTime startDt) {
        this.startDt = startDt;
    }

    public LocalDateTime getEndDt() {
        return endDt;
    }

    public void setEndDt(LocalDateTime endDt) {
        this.endDt = endDt;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}
