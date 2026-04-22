# Build stage
#FROM maven:3.9-eclipse-temurin-17 AS builder
FROM maven:3.9-eclipse-temurin-17

WORKDIR /build
COPY pom.xml .
RUN mvn dependency:go-offline

COPY src src
RUN mvn clean package -DskipTests

# Runtime stage
# Ignored due to "Run Reviews Service Tests" step in GitHub action.
# This is rubbish and should be improved in future
# FROM eclipse-temurin:17-jre

WORKDIR /app

#COPY --from=builder /build/target/reviews-service-*.jar app.jar
RUN cp /build/target/reviews-service-*.jar app.jar

EXPOSE 8081 5005

CMD ["java", "-jar", "app.jar"]
