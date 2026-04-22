# Build stage
FROM maven:3.9-eclipse-temurin-17 AS builder

WORKDIR /build
COPY pom.xml .
RUN mvn dependency:go-offline

COPY src src
RUN mvn clean package -DskipTests

# Runtime stage
FROM eclipse-temurin:17-jre

WORKDIR /app
COPY --from=builder /build/target/reviews-service-*.jar app.jar

# For "Run Reviews Service Tests" step in GitHub action.
# This is rubbish and should be improved in future
RUN apt-get update && apt-get install -y maven && rm -rf /var/lib/apt/lists/*

EXPOSE 8081 5005

CMD ["java", "-jar", "app.jar"]
