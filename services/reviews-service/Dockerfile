FROM maven:3.9-eclipse-temurin-17

WORKDIR /build
COPY pom.xml .
RUN mvn dependency:go-offline

COPY src src
RUN mvn clean package -DskipTests

WORKDIR /app

RUN cp /build/target/reviews-service-*.jar app.jar

EXPOSE 8081 5005

CMD ["java", "-jar", "app.jar"]
