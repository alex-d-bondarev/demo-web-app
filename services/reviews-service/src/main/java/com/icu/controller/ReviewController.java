package com.icu.controller;

import com.icu.model.Review;
import com.icu.model.ReviewItem;
import com.icu.repository.ReviewRepository;
import com.icu.repository.ReviewItemRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.List;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping
@CrossOrigin(origins = "http://localhost:9010")
public class ReviewController {

    @Autowired
    private ReviewRepository reviewRepository;

    @Autowired
    private ReviewItemRepository reviewItemRepository;

    // ============= REVIEW ENDPOINTS =============

    /**
     * GET /review - List all reviews
     */
    @GetMapping("/review")
    public ResponseEntity<?> getAllReviews() {
        try {
            List<Review> reviews = reviewRepository.findAll();
            return ResponseEntity.ok(reviews);
        } catch (Exception e) {
            return handleException(e);
        }
    }

    /**
     * POST /review - Create new review
     */
    @PostMapping("/review")
    @Transactional
    public ResponseEntity<?> createReview(@RequestBody Review review) {
        try {
            review.setReviewId(null);
            reviewRepository.save(review);
            Map<String, String> response = new HashMap<>();
            response.put("status", "created");
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return handleException(e);
        }
    }

    /**
     * PUT /review/{review_id} - Update review
     */
    @PutMapping("/review/{review_id}")
    @Transactional
    public ResponseEntity<?> updateReview(@PathVariable Integer review_id, @RequestBody Review review) {
        try {
            if (!reviewRepository.existsById(review_id)) {
                return handleException(new RuntimeException("Review not found"));
            }
            review.setReviewId(review_id);
            reviewRepository.save(review);
            Map<String, String> response = new HashMap<>();
            response.put("status", "updated");
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return handleException(e);
        }
    }

    /**
     * DELETE /review/{review_id} - Delete review
     */
    @DeleteMapping("/review/{review_id}")
    @Transactional
    public ResponseEntity<?> deleteReview(@PathVariable Integer review_id) {
        try {
            reviewRepository.deleteById(review_id);
            Map<String, String> response = new HashMap<>();
            response.put("status", "deleted");
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return handleException(e);
        }
    }

    // ============= REVIEW ITEM ENDPOINTS =============

    /**
     * GET /review/{review_id}/item - Get all review items for a review
     */
    @GetMapping("/review/{review_id}/item")
    public ResponseEntity<?> getReviewItems(@PathVariable Integer review_id) {
        try {
            List<ReviewItem> reviewItems = reviewItemRepository.findByReviewId(review_id);
            return ResponseEntity.ok(reviewItems);
        } catch (Exception e) {
            return handleException(e);
        }
    }

    /**
     * POST /review/{review_id}/item/{review_item_id} - Add item to review
     */
    @PostMapping("/review/{review_id}/item/{review_item_id}")
    @Transactional
    public ResponseEntity<?> addReviewItem(
            @PathVariable Integer review_id,
            @PathVariable Integer review_item_id,
            @RequestBody ReviewItem reviewItem) {
        try {
            reviewItemRepository.save(reviewItem);
            Map<String, String> response = new HashMap<>();
            response.put("status", "added");
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return handleException(e);
        }
    }

    /**
     * DELETE /review/{review_id}/item/{review_item_id} - Delete review item
     */
    @DeleteMapping("/review/{review_id}/item/{review_item_id}")
    @Transactional
    public ResponseEntity<?> deleteReviewItem(
            @PathVariable Integer review_id,
            @PathVariable Integer review_item_id) {
        try {
            reviewItemRepository.deleteById(review_item_id);
            Map<String, String> response = new HashMap<>();
            response.put("status", "deleted");
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return handleException(e);
        }
    }

    // ============= HEALTH CHECK =============

    /**
     * GET /health - Health check endpoint
     */
    @GetMapping("/health")
    public ResponseEntity<?> health() {
        try {
            Map<String, String> response = new HashMap<>();
            response.put("status", "ok");
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            return handleException(e);
        }
    }

    // ============= ERROR HANDLING =============

    /**
     * Handle exceptions - return HTTP 200 with error status
     */
    private ResponseEntity<?> handleException(Exception e) {
        Map<String, String> errorResponse = new HashMap<>();
        errorResponse.put("status", "error");
        errorResponse.put("message", e.getMessage());
        return ResponseEntity.ok(errorResponse);
    }
}
