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

* **Spring Boot DevTools Developer**
  * Provides fast application restarts, LiveReload, and configurations for enhanced development experience.
  * development help
---
* **Spring Web**
  * Build web, including RESTful, applications using Spring MVC. Uses Apache Tomcat as the default embedded container.
  * web application
* **Lombok**
  * Java annotation library which helps to reduce boilerplate code.
  * boilerplate code reduction
* **Docker Compose Support**
  * Provides docker compose support for enhanced development experience.
  * docker compose integration
* **Spring Security**
  * Highly customizable authentication and access-control framework for Spring applications.
  * security framework
---
* **Spring Data JPA**
  * Persist data in SQL stores with Java Persistence API using Spring Data and Hibernate.
* **Flyway Migration**
  * Version control for your database so you can migrate from any version (incl. an empty database) to the latest version of the schema.
* **PostgreSQL Driver**
  * A JDBC and R2DBC driver that allows Java programs to connect to a PostgreSQL database using standard, database independent Java code.
---
* **OpenFeign Spring Cloud**
  * Declarative REST Client. OpenFeign creates a dynamic implementation of an interface decorated with JAX-RS or Spring MVC annotations.
* **OAuth2 Client**
  * Spring Boot integration for Spring Security's OAuth2/OpenID Connect client features.
---
* **Rest Repositories HAL Explorer**
  * Provides a simple, web-based UI for navigating hypermedia APIs built with Spring Data REST.
  * hypermedia API exploration
* **Spring Boot Actuator**
  * Supports built in (or custom) endpoints that let you monitor and manage your application - such as application health, metrics, sessions, etc.


https://www.baeldung.com/spring-rest-openapi-documentation