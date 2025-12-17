# Auditable Mapped Field Snippet


```java
  @CreatedBy
  @Column(
    name = "created_by",
    nullable = false,
    updatable = false
  )
  private String createdBy;
  @CreatedDate
  @Column(
    name = "created_date",
    nullable = false,
    updatable = false
  )
  private OffsetDateTime createdDate;
  @LastModifiedBy
  @Column(
    name = "modified_by"
  )
  private String modifiedBy;
  @LastModifiedDate
  @Column(
    name = "modified_date"
  )
  private OffsetDateTime modifiedDate;
```

## Project settings

* **Spring Boot DevTools Developer Tools**
  * Provides fast application restarts, LiveReload, and configurations for enhanced development experience.
  * development help
---
* **Spring Web Web**
    * Build web, including RESTful, applications using Spring MVC. Uses Apache Tomcat as the default embedded container.
    * web application
* **Lombok Developer Tools**
    * Java annotation library which helps to reduce boilerplate code.
    * boilerplate code reduction
* **Docker Compose Support Developer Tools**
    * Provides docker compose support for enhanced development experience.
    * docker compose integration
* **Spring Security Security**
  * Highly customizable authentication and access-control framework for Spring applications.
  * security framework
---
* **Spring Data JPA SQL**
  * Persist data in SQL stores with Java Persistence API using Spring Data and Hibernate.
* **Flyway Migration SQL**
  * Version control for your database so you can migrate from any version (incl. an empty database) to the latest version of the schema.
* **PostgreSQL Driver SQL**
  * A JDBC and R2DBC driver that allows Java programs to connect to a PostgreSQL database using standard, database independent Java code.
---
* **OpenFeign Spring Cloud Routing**
  * Declarative REST Client. OpenFeign creates a dynamic implementation of an interface decorated with JAX-RS or Spring MVC annotations.
* **OAuth2 Client Security**
  * Spring Boot integration for Spring Security's OAuth2/OpenID Connect client features.

https://www.baeldung.com/spring-rest-openapi-documentation