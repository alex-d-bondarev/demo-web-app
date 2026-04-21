package com.icu;

import com.icu.controller.ReviewController;
import com.icu.model.Review;
import com.icu.model.ReviewItem;
import com.icu.repository.ReviewRepository;
import com.icu.repository.ReviewItemRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import java.time.LocalDateTime;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
public class ReviewsControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ReviewRepository reviewRepository;

    @Autowired
    private ReviewItemRepository reviewItemRepository;

    @Test
    public void testGetAllReviewsReturns200() throws Exception {
        mockMvc.perform(get("/review"))
            .andExpect(status().isOk());
    }

    @Test
    public void testPostReviewReturnsCreatedStatus() throws Exception {
        String payload = """
            {
                "review_id": 1,
                "start_dt": "2024-01-01T10:00:00",
                "end_dt": "2024-01-05T15:30:00",
                "status": "completed"
            }
            """;
        
        mockMvc.perform(post("/review")
            .contentType(MediaType.APPLICATION_JSON)
            .content(payload))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.status").value("created"));
    }

    @Test
    public void testDeleteReviewReturns200() throws Exception {
        mockMvc.perform(delete("/review/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.status").value("deleted"));
    }

    @Test
    public void testGetReviewItemsReturns200() throws Exception {
        mockMvc.perform(get("/review/1/item"))
            .andExpect(status().isOk());
    }

    @Test
    public void testPostReviewItemReturnsAddedStatus() throws Exception {
        String payload = """
            {
                "review_item_id": 1,
                "review_id": 1,
                "item_id": 1,
                "quantity": 50
            }
            """;
        
        mockMvc.perform(post("/review/1/item/1")
            .contentType(MediaType.APPLICATION_JSON)
            .content(payload))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.status").value("added"));
    }

    @Test
    public void testDeleteReviewItemReturns200() throws Exception {
        mockMvc.perform(delete("/review/1/item/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.status").value("deleted"));
    }

    @Test
    public void testHealthCheckReturns200() throws Exception {
        mockMvc.perform(get("/health"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.status").value("ok"));
    }
}
