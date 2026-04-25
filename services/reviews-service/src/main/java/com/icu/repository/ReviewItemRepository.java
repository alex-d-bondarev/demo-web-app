package com.icu.repository;

import com.icu.model.ReviewItem;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface ReviewItemRepository extends JpaRepository<ReviewItem, Integer> {
    @Query("SELECT ri FROM ReviewItem ri WHERE ri.reviewId = :reviewId")
    List<ReviewItem> findByReviewId(@Param("reviewId") Integer reviewId);
}
