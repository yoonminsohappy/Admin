DROP DATABASE IF EXISTS brandi;
CREATE DATABASE brandi;
USE brandi;

-- 셀러 속성
CREATE TABLE seller_properties
(
    `id`    INT            NOT NULL    AUTO_INCREMENT COMMENT 'pk', 
    `name`  VARCHAR(45)    NOT NULL    COMMENT '이름', 
    PRIMARY KEY (id)
);

ALTER TABLE seller_properties COMMENT '셀러 속성';

-- 셀러 상태
CREATE TABLE seller_statuses
(
    `id`    INT            NOT NULL    AUTO_INCREMENT COMMENT 'pk', 
    `name`  VARCHAR(64)    NOT NULL    COMMENT '이름', 
    PRIMARY KEY (id)
);

ALTER TABLE seller_statuses COMMENT '셀러 상태';

-- 은행 
CREATE TABLE banks
(
    `id`    INT            NOT NULL    AUTO_INCREMENT COMMENT 'pk',  
    `name`  VARCHAR(64)    NOT NULL    COMMENT '이름', 
    PRIMARY KEY (id)
);

ALTER TABLE banks COMMENT '은행 이름';

-- 셀러 유저
CREATE TABLE sellers
(
    `id`                           INT              NOT NULL    AUTO_INCREMENT COMMENT '셀러번호', 
    `register_date`                DATETIME         NOT NULL    DEFAULT NOW() COMMENT '등록일시', 
    `seller_status_id`             INT              NOT NULL    COMMENT '셀러 상태 아이디', 
    `is_master`                    BOOLEAN          NOT NULL    DEFAULT False COMMENT '마스터', 
    `is_deleted`                   BOOLEAN          NOT NULL    DEFAULT False COMMENT '삭제 여부', 
    `seller_account`               VARCHAR(128)     NOT NULL    COMMENT '셀러 계정', 
    `english_name`                 VARCHAR(128)     NOT NULL    COMMENT '영문이름', 
    `korean_name`                  VARCHAR(128)     NOT NULL    COMMENT '한글 이름', 
    `cs_phone`                     VARCHAR(64)      NOT NULL    COMMENT '고객센터 전화번호', 
    `seller_property_id`           INT              NOT NULL    COMMENT '셀러 속성 아이디', 
    `profile_image`                VARCHAR(2048)    NULL        COMMENT '프로필이미지URL', 
    `password`                     VARCHAR(256)     NULL        COMMENT '패스워드', 
    `background_image`             VARCHAR(2048)    NOT NULL    COMMENT '셀러페이지배경이미지URL', 
    `simple_description`           TEXT             NOT NULL    COMMENT '한줄소개', 
    `detail_description`           TEXT             NOT NULL    COMMENT '상세소개', 
    `zip_code`                     VARCHAR(32)      NOT NULL    COMMENT '우편번호', 
    `address`                      VARCHAR(256)     NOT NULL    COMMENT '주소', 
    `detail_address`               VARCHAR(512)     NOT NULL    COMMENT '상세주소', 
    `open_time`                    TIME             NOT NULL    COMMENT '운영시작시간', 
    `close_time`                   TIME             NOT NULL    COMMENT '운영마감시간', 
    `bank_id`                      INT              NOT NULL    COMMENT '은행 아이디', 
    `account_number`               VARCHAR(128)     NOT NULL    COMMENT '계좌번호', 
    `account_name`                 VARCHAR(128)     NOT NULL    COMMENT '계좌주인이름', 
    `shipping_information`         TEXT             NOT NULL    COMMENT '배송정보', 
    `exchange_refund_information`  TEXT             NOT NULL    COMMENT '교환/환불정보', 
    `model_height`                 VARCHAR(32)      NULL        COMMENT '모델키', 
    `model_top_size`               VARCHAR(32)      NULL        COMMENT '모델상의사이즈', 
    `model_bottom_size`            VARCHAR(32)      NULL        COMMENT '모델하의사이즈', 
    `model_feet_size`              VARCHAR(32)      NULL        COMMENT '모델신발사이즈', 
    `shopping_feedtext`            TEXT             NULL        COMMENT '쇼핑피드텍스트', 
    `registered_product_count`     INT              NOT NULL    DEFAULT 0 COMMENT '등록상품개수', 
    `created_at`                   DATETIME         NOT NULL    DEFAULT CURRENT_TIMESTAMP COMMENT '선분이력 시작일자',
    `expired_at`                   DATETIME         NOT NULL    DEFAULT '9999-12-31 23:59:59' COMMENT '선분이력 종료일자', 
    `modifier_id`                  INT              NULL        COMMENT '수정자아이디', 
    PRIMARY KEY (id)
);

ALTER TABLE sellers COMMENT '셀러 유저';

ALTER TABLE sellers
    ADD CONSTRAINT FK_sellers_seller_status_id_seller_statuses_id FOREIGN KEY (seller_status_id)
        REFERENCES seller_statuses (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE sellers
    ADD CONSTRAINT FK_sellers_seller_property_id_seller_properties_id FOREIGN KEY (seller_property_id)
        REFERENCES seller_properties (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE sellers
    ADD CONSTRAINT FK_sellers_bank_id_banks_id FOREIGN KEY (bank_id)
        REFERENCES banks (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE sellers
    ADD CONSTRAINT FK_sellers_modifier_id_sellers_id FOREIGN KEY (modifier_id)
        REFERENCES sellers (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- 셀러 담당자
CREATE TABLE seller_managers
(
    `id`            INT             NOT NULL    AUTO_INCREMENT, 
    `name`          VARCHAR(64)     NOT NULL    COMMENT '이름', 
    `phone_number`  VARCHAR(64)     NOT NULL    COMMENT '전화번호', 
    `email`         VARCHAR(128)    NOT NULL    COMMENT '이메일', 
    `seller_id`     INT             NOT NULL    COMMENT '셀러아이디', 
    PRIMARY KEY (id)
);

ALTER TABLE seller_managers COMMENT '셀러 담당자';

ALTER TABLE seller_managers
    ADD CONSTRAINT FK_seller_managers_seller_id_sellers_id FOREIGN KEY (seller_id)
        REFERENCES sellers (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- 셀러 상태 변경 이력
CREATE TABLE seller_status_modification_histories
(
    `id`                INT         NOT NULL    AUTO_INCREMENT, 
    `seller_id`         INT         NOT NULL    COMMENT '셀러 아이디', 
    `updated_at`        DATETIME    NOT NULL    COMMENT '셀러 상태에 따라 사용하기', 
    `seller_status_id`  INT         NOT NULL    COMMENT '셀러 상태 아이디', 
    `modifier_id`       INT         NOT NULL    COMMENT '수정자 아이디', 
    PRIMARY KEY (id)
);

ALTER TABLE seller_status_modification_histories  COMMENT '셀러상태 변경이력';

ALTER TABLE seller_status_modification_histories
    ADD CONSTRAINT seller_status_modification_histories_seller_status_id FOREIGN KEY (seller_status_id)
        REFERENCES seller_statuses (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE seller_status_modification_histories
    ADD CONSTRAINT seller_status_modification_histories_seller_id FOREIGN KEY (seller_id)
        REFERENCES sellers (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE seller_status_modification_histories
    ADD CONSTRAINT seller_status_modification_histories_modifier_id FOREIGN KEY (modifier_id)
        REFERENCES sellers (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- 2차 카테고리
CREATE TABLE second_categories
(
    `id`    INT            NOT NULL    AUTO_INCREMENT COMMENT 'pk', 
    `name`  VARCHAR(45)    NOT NULL    COMMENT '이름', 
    PRIMARY KEY (id)
);

ALTER TABLE second_categories COMMENT '2차 카테고리';

-- 1차 카테고리
CREATE TABLE first_categories
(
    `id`    INT            NOT NULL    AUTO_INCREMENT COMMENT 'pk', 
    `name`  VARCHAR(64)    NOT NULL    COMMENT '이름', 
    PRIMARY KEY (id)
);

ALTER TABLE first_categories COMMENT '1차 카테고리';

-- 1차 카테고리 & 2차 카테고리 중간 테이블
CREATE TABLE first_category_second_categories
(
    `id`                  INT    NOT NULL    AUTO_INCREMENT COMMENT 'pk', 
    `first_category_id`   INT    NOT NULL    COMMENT '1차 카테고리 아이디', 
    `second_category_id`  INT    NOT NULL    COMMENT '2차 카테고리 아이디', 
    PRIMARY KEY (id)
);

ALTER TABLE first_category_second_categories COMMENT '1차 & 2차 카테고리 중간 테이블';

-- 위의 중간 테이블과 1차 카테고리 연결
ALTER TABLE first_category_second_categories
    ADD CONSTRAINT FK_fcsc_first_category FOREIGN KEY (first_category_id)
        REFERENCES first_categories (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- 위의 중간 테이블과 2차 카테고리 연결
ALTER TABLE first_category_second_categories
    ADD CONSTRAINT FK_fcsc_second_category FOREIGN KEY (second_category_id)
        REFERENCES second_categories (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- 1차 카테고리 & 셀러 속성 테이블
CREATE TABLE first_category_seller_properties
(
    `id`                  INT     NOT NULL    AUTO_INCREMENT, 
    `first_category_id`   INT     NOT NULL    COMMENT '1차 카테고리 아이디', 
    `seller_property_id`  INT     NOT NULL    COMMENT '셀러 속성 아이디', 
    PRIMARY KEY (id)
);

ALTER TABLE first_category_seller_properties COMMENT '1차 카테고리 & 셀러 중간 테이블';

ALTER TABLE first_category_seller_properties
    ADD CONSTRAINT FK_fcsp_seller_property_id FOREIGN KEY (seller_property_id)
        REFERENCES seller_properties (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE first_category_seller_properties
    ADD CONSTRAINT FK_fcsc_first_category_id FOREIGN KEY (first_category_id)
        REFERENCES first_categories (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

CREATE TABLE country_of_origins
(
    `id`    INT            NOT NULL    AUTO_INCREMENT COMMENT 'pk', 
    `name`  VARCHAR(64)    NOT NULL    COMMENT '이름', 
    PRIMARY KEY (id)
);

ALTER TABLE country_of_origins COMMENT '원산지 국가';

-- 상품
CREATE TABLE products
(
    `id`             INT             NOT NULL    AUTO_INCREMENT COMMENT 'pk', 
    `sale_amount`    INT             NOT NULL    DEFAULT 0 COMMENT '판매량', 
    `register_date`  DATETIME        NOT NULL    DEFAULT CURRENT_TIMESTAMP COMMENT '등록일', 
    `code`           VARCHAR(128)    NOT NULL    COMMENT '상품코드', 
    `review_count`   INT             NOT NULL    DEFAULT 0 COMMENT '리뷰 개수', 
    `qna_count`      INT             NOT NULL    DEFAULT 0 COMMENT 'Q&A 개수', 
    `is_deleted`     BOOLEAN         NOT NULL    DEFAULT 0 COMMENT '삭제 여부', 
    `seller_id`      INT             NOT NULL    COMMENT '셀러 아이디', 
    `categories_id`  INT             NOT NULL    COMMENT '1차 & 2차 카테고리 중간 테이블 id',
    PRIMARY KEY (id)
);

ALTER TABLE products COMMENT '상품';

-- 상품과 1차 & 2차카테고리 중간 테이블 연결
ALTER TABLE products
    ADD CONSTRAINT FK_products_categories_id FOREIGN KEY (categories_id)
        REFERENCES first_category_second_categories (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- 상품 상세
CREATE TABLE product_details
(
    `id`                    INT             NOT NULL    AUTO_INCREMENT COMMENT 'pk', 
    `name`                  VARCHAR(64)     NOT NULL    COMMENT '상품명',
    `is_sold`               BOOLEAN         NOT NULL    DEFAULT 0 COMMENT '판매 여부', 
    `is_displayed`          BOOLEAN         NOT NULL    DEFAULT 0 COMMENT '진열 여부', 
    `origin_company`        VARCHAR(128)    NULL        COMMENT '제조사', 
    `origin_date`           DATE            NULL        COMMENT '제조일자',   
    `simple_description`    VARCHAR(256)    NULL        COMMENT '한줄설명', 
    `description`           LONGTEXT        NOT NULL    COMMENT '상세설명',   
    `sale_price`            INT             NOT NULL    COMMENT '판매가', 
    `discount_rate`         INT             NOT NULL    DEFAULT 0 COMMENT '할인율', 
    `discount_started_at`   DATETIME        NULL        COMMENT '할인시작날짜', 
    `discount_ended_at`     DATETIME        NULL        COMMENT '할인종료날짜', 
    `minimum_sale_amount`   TINYINT         NOT NULL    COMMENT '최소판매수량', 
    `maximum_sale_amount`   TINYINT         NOT NULL    COMMENT '최대판매수량',
    `created_at`            DATETIME        NOT NULL    DEFAULT CURRENT_TIMESTAMP COMMENT '선분이력 시작일자', 
    `expired_at`            DATETIME        NOT NULL    DEFAULT '9999-12-31 23:59:59' COMMENT '선분이력 종료일자',
    `modifier_id`           INT             NOT NULL    COMMENT '수정자 아이디',
    `product_id`            INT             NOT NULL    COMMENT '상품 아이디', 
    `country_of_origin_id`  INT             NULL        COMMENT '제조국 아이디',
    PRIMARY KEY (id)
);

ALTER TABLE product_details COMMENT '상품 상세 정보';

ALTER TABLE product_details
    ADD CONSTRAINT FK_product_detail_product_id_ FOREIGN KEY (product_id)
        REFERENCES products (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE product_details
    ADD CONSTRAINT FK_product_detail_country_of_origin_id FOREIGN KEY (country_of_origin_id)
        REFERENCES country_of_origins (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE product_details
    ADD CONSTRAINT FK_product_detail_modifier_id FOREIGN KEY (modifier_id)
        REFERENCES sellers (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- 상품 이미지 테이블
CREATE TABLE product_images
(
    `id`          INT            NOT NULL    AUTO_INCREMENT COMMENT 'pk',  
    `image_path`  VARCHAR(2048)    NOT NULL    COMMENT 'URL', 
    `ordering`    TINYINT        NOT NULL    COMMENT '이미지 순서', 
    `product_id`  INT            NOT NULL    COMMENT '상품 아이디',
    PRIMARY KEY (id)
);

ALTER TABLE product_images COMMENT '상품 이미지';

ALTER TABLE product_images
    ADD CONSTRAINT FK_product_images_product_id FOREIGN KEY (product_id)
        REFERENCES products (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- 상품 컬러 테이블
CREATE TABLE colors
(
    `id`    INT            NOT NULL    AUTO_INCREMENT COMMENT 'pk', 
    `name`  VARCHAR(128)   NOT NULL    COMMENT '이름', 
    PRIMARY KEY (id)
);

ALTER TABLE colors COMMENT '상품 색상';

-- 상품 사이즈 테이블
CREATE TABLE sizes
(
    `id`    INT            NOT NULL    AUTO_INCREMENT COMMENT 'pk', 
    `name`  VARCHAR(128)   NOT NULL    COMMENT '이름', 
    PRIMARY KEY (id)
);

ALTER TABLE sizes COMMENT '상품 사이즈';

-- 상품에 딸린 옵션
CREATE TABLE options
(
    `id`          INT    NOT NULL    AUTO_INCREMENT COMMENT 'pk', 
    `stock`       INT    NULL        DEFAULT 0 COMMENT '재고', 
    `product_id`  INT    NOT NULL    COMMENT '상품 아이디',
    `color_id`    INT    NOT NULL    COMMENT '색상 아이디', 
    `size_id`     INT    NOT NULL    COMMENT '사이즈 아이디', 
    PRIMARY KEY (id)
);

ALTER TABLE options COMMENT '상품 옵션';

ALTER TABLE options
    ADD CONSTRAINT FK_options_product_id_products_id FOREIGN KEY (product_id)
        REFERENCES products (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE options
    ADD CONSTRAINT FK_options_color_id_colors_id FOREIGN KEY (color_id)
        REFERENCES colors (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE options
    ADD CONSTRAINT FK_options_size_id_sizes_id FOREIGN KEY (size_id)
        REFERENCES sizes (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- 쿠폰
CREATE TABLE issue_types
(
    `id`    INT            NOT NULL    AUTO_INCREMENT, 
    `name`  VARCHAR(64)    NOT NULL, 
    PRIMARY KEY (id)
);
ALTER TABLE issue_types COMMENT '일반, 쿠폰코드, 시리얼번호';

-- coupons Table Create SQL
CREATE TABLE coupons
(
    `id`                   INT            NOT NULL    AUTO_INCREMENT, 
    `name`                 VARCHAR(64)    NOT NULL    			COMMENT '쿠폰이름', 
    `started_at`           DATETIME       NOT NULL    			COMMENT '쿠폰 유효 시작일', 
    `ended_at`             DATETIME       NOT NULL    			COMMENT '쿠폰 유효 종료일', 
    `discount_option`      INT            NOT NULL    			COMMENT '원(won)', 
    `download_started_at`  DATETIME       NOT NULL    			COMMENT '다운로드 시작일', 
    `download_expired_at`  DATETIME       NOT NULL    			COMMENT '다운로드 종료일', 
    `issue_type_id`        INT            NOT NULL    			COMMENT '발급 유형 아이디', 
    `description`          TEXT           NOT NULL    			COMMENT '상세설명', 
    `is_limited`           TINYINT(1)     NOT NULL    			COMMENT 'true/false', 
    `limit_count`          INT            NULL        			COMMENT 'null = 무한대', 
    `minimum_price`        INT            NOT NULL    			COMMENT '최소사용가능금액', 
    `download_count`       INT            NOT NULL    			COMMENT 'download한 개수', 
    `use_count`            INT            NOT NULL    			COMMENT 'default = 0', 
    `is_downloadable`      TINYINT(1)     NOT NULL    			COMMENT '다운로드or직접발급', 
    `updated_at`           DATETIME       NOT NULL    DEFAULT NOW()    	COMMENT '수정 일자', 
    `modifier_id`          INT            NOT NULL    			COMMENT '수정자 아이디', 
    PRIMARY KEY (id)
);
ALTER TABLE coupons COMMENT '기획전';

ALTER TABLE coupons
    ADD CONSTRAINT FK_coupons_issue_type_id FOREIGN KEY (issue_type_id)
        REFERENCES issue_types (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- event_types Table Create SQL
CREATE TABLE event_types
(
    `id`    INT            NOT NULL    AUTO_INCREMENT, 
    `name`  VARCHAR(64)    NOT NULL, 
    PRIMARY KEY (id)
);
ALTER TABLE event_types COMMENT '이벤트, 쿠폰, 상품(이미지), 상품(텍스트), 유튜브';

-- event_statuses Table Create SQL
CREATE TABLE event_statuses
(
    `id`    INT            NOT NULL    AUTO_INCREMENT, 
    `name`  VARCHAR(64)    NOT NULL    COMMENT '진행 상태 이름', 
    PRIMARY KEY (id)
);
ALTER TABLE event_statuses COMMENT '진행중 / 종료 / 대기';

-- events Table Create SQL
CREATE TABLE events
(
    `id`                    INT              NOT NULL    AUTO_INCREMENT, 
    `name`                  VARCHAR(256)     NOT NULL    			COMMENT '기획전명', 
    `event_status_id`       INT              NOT NULL    			COMMENT '기획전 진행 상태', 
    `event_type_id`         INT              NOT NULL    			COMMENT '기획전 타입', 
    `register_date`         DATETIME         NOT NULL    			COMMENT '기획전 등록일', 
    `started_at`            DATETIME         NOT NULL    			COMMENT '기획전 시작일', 
    `ended_at`              DATETIME         NOT NULL    			COMMENT '기획전 종료일', 
    `is_event_exposed`      TINYINT          NOT NULL    			COMMENT '노출여부', 
    `banner_image_url`      VARCHAR(2048)    NOT NULL   			COMMENT '배너이미지', 
    `detail_image`          LONGTEXT         NOT NULL    			COMMENT '상세이미지', 
    `modifier_id`           INT              NOT NULL    			COMMENT '수정자 아이디', 
    `created_at`            DATETIME         NOT NULL    DEFAULT NOW()		COMMENT '선분이력시작일자', 
    `expired_at`            DATETIME         NOT NULL    DEFAULT '9999-12-31'	COMMENT '최신 9999-12-31', 
    `mapped_product_count`  INT              NOT NULL    			COMMENT 'default = 0', 
    `view_count`            INT              NOT NULL    			COMMENT '조회수', 
    PRIMARY KEY (id)
);
ALTER TABLE events COMMENT '기획전';
ALTER TABLE events
    ADD CONSTRAINT FK_event_type_id FOREIGN KEY (event_type_id)
        REFERENCES event_types (id) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE events
    ADD CONSTRAINT FK_event_status_id FOREIGN KEY (event_status_id)
        REFERENCES event_statuses (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- event_buttons Table Create SQL
CREATE TABLE event_buttons
(
    `id`        INT            NOT NULL    AUTO_INCREMENT, 
    `name`      VARCHAR(64)    NOT NULL    COMMENT '버튼 이름', 
    `order`     INT            NOT NULL    COMMENT '버튼 진열 순위', 
    `event_id`  INT            NOT NULL    COMMENT '이벤트 아이디', 
    `is_exist`  boolean        NOT NULL    COMMENT '버튼존재여부', 
    PRIMARY KEY (id)
);
ALTER TABLE event_buttons
    ADD CONSTRAINT FK_buttons_event_id FOREIGN KEY (event_id)
        REFERENCES events (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- event_kinds Table Create SQL
CREATE TABLE event_kinds
(
    `id`             INT            NOT NULL    AUTO_INCREMENT, 
    `name`           VARCHAR(64)    NOT NULL, 
    `event_type_id`  INT            NOT NULL    COMMENT '기획전 타입 아이디', 
    PRIMARY KEY (id)
);
ALTER TABLE event_kinds COMMENT '댓글창있음/없음, 쿠폰은 만들어진거, 상품/버튼, 상품/버튼, 상품/버튼';
ALTER TABLE event_kinds
    ADD CONSTRAINT FK_kinds_event_type_id FOREIGN KEY (event_type_id)
        REFERENCES event_types (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- product_events Table Create SQL
CREATE TABLE product_events
(
    `id`          INT    NOT NULL    AUTO_INCREMENT, 
    `product_id`  INT    NOT NULL    COMMENT '상품아이디', 
    `order`       INT    NOT NULL    COMMENT '진열순위', 
    `button_id`   INT    NOT NULL    COMMENT '버튼없을때하나생성', 
    PRIMARY KEY (id)
);
ALTER TABLE product_events COMMENT '상품';
ALTER TABLE product_events
    ADD CONSTRAINT FK_product_events_button_id FOREIGN KEY (button_id)
        REFERENCES event_buttons (id) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE product_events
    ADD CONSTRAINT FK_events_product_id FOREIGN KEY (product_id)
        REFERENCES products (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- second_categories Table Create SQL
CREATE TABLE product_coupons
(
    `id`          INT    NOT NULL    AUTO_INCREMENT COMMENT '아이디', 
    `product_id`  INT    NOT NULL    COMMENT '상품 아이디', 
    `coupon_id`   INT    NOT NULL    COMMENT '쿠폰 아이디', 
    PRIMARY KEY (id)
);
ALTER TABLE product_coupons
    ADD CONSTRAINT FK_product_coupons_coupon_id FOREIGN KEY (coupon_id)
        REFERENCES coupons (id) ON DELETE RESTRICT ON UPDATE RESTRICT;
ALTER TABLE product_coupons
    ADD CONSTRAINT FK_product_coupons_product_id FOREIGN KEY (product_id)
        REFERENCES products (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- 유저
CREATE TABLE users
(
    `id`             INT             NOT NULL    AUTO_INCREMENT   COMMENT '고유아이디',
    `account_id`     VARCHAR(64)     NOT NULL                     COMMENT '회원 아이디',
    `register_date`  DATETIME        NOT NULL    Default NOW()    COMMENT '날짜 + 시간',
    `is_deleted`     BOOLEAN         NOT NULL    Default False,
    `last_name`      VARCHAR(64)     NOT NULL                     COMMENT '성',
    `first_name`     VARCHAR(64)     NOT NULL                     COMMENT '이름',
    `email`          VARCHAR(128)    NOT NULL                     COMMENT '이메일',
    `password`       BIT             NULL                         COMMENT '패스워드',
    `created_at`     DATETIME        NOT NULL    Default NOW()    COMMENT '선분이력시작일자',
    `expired_at`     DATETIME        NOT NULL                     COMMENT '선분이력종료일자',
    `phone_number`   VARCHAR(32)     NULL                         COMMENT '휴대폰 번호',
    `modifier_id`    INT             NULL                         COMMENT '마스터가 바꿀 수 있음',
    PRIMARY KEY (id)
);
ALTER TABLE users COMMENT '서비스 사용자 테이블';
ALTER TABLE users
    ADD CONSTRAINT FK_users_modifier_id_sellers_id FOREIGN KEY (modifier_id)
        REFERENCES sellers (id) ON DELETE RESTRICT ON UPDATE RESTRICT;
CREATE TABLE shipping_informations
(
    `id`             INT             NOT NULL                   AUTO_INCREMENT,
    `name`           VARCHAR(64)     NOT NULL                   COMMENT '수령인 이름',
    `phone_number`   VARCHAR(64)     NOT NULL                   COMMENT '수취인 휴대폰',
    `address`        VARCHAR(256)    NOT NULL                   COMMENT '주소',
    `shipping_memo`  VARCHAR(128)    NULL                       COMMENT '배송 메모',
    `user_id`        INT             NOT NULL                   COMMENT '유저아이디',
    `is_deleted`     BOOLEAN         NULL        Default False,
    PRIMARY KEY (id)
);
ALTER TABLE shipping_informations COMMENT '배송지 정보';
ALTER TABLE shipping_informations
    ADD CONSTRAINT FK_shipping_informations_user_id_users_id FOREIGN KEY (user_id)
        REFERENCES users (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

CREATE TABLE wearing_sensations
(
    `id`       INT            NOT NULL    AUTO_INCREMENT COMMENT '아이디', 
    `content`  VARCHAR(45)    NULL        COMMENT '내용', 
    PRIMARY KEY (id)
);

ALTER TABLE wearing_sensations COMMENT '착용감 아이디';        

CREATE TABLE reviews
(
    `id`                    INT             NOT NULL                     AUTO_INCREMENT,
    `user_id`               INT             NOT NULL                     COMMENT '유저아이디',
    `product_id`            INT             NOT NULL                     COMMENT '상품아이디',
    `content`               TEXT            NOT NULL                     COMMENT '리뷰내용',
    `register_date`         DATETIME        NOT NULL    Default NOW()    COMMENT '등록 일자',
    `updated_at`            DATETIME        NOT NULL                     COMMENT '수정일자',
    `grade`                 INT             NOT NULL                     COMMENT '1-5',
    `is_deleted`            BOOLEAN         NOT NULL    Default False    COMMENT '삭제 여부',
    `modifier_id`           INT             NULL                         COMMENT '수정자 아이디',
    `option_text`           VARCHAR(128)    NOT NULL                     COMMENT '옵션을 텍스트 리터럴로 저장',
    `wearing_sensation_id`  INT(128)        NOT NULL                     COMMENT '착용감 아이디',
    `height`                VARCHAR(32)     NOT NULL                     COMMENT '키',
    `top`                   VARCHAR(32)     NOT NULL                     COMMENT '상의',
    `bottom`                VARCHAR(32)     NOT NULL                     COMMENT '하의',
    `shoe_size`             VARCHAR(32)     NOT NULL                     COMMENT '신발사이즈',
    PRIMARY KEY (id)
);
ALTER TABLE reviews COMMENT '텍스트 리뷰';

ALTER TABLE reviews
    ADD CONSTRAINT FK_reviews_user_id_users_id FOREIGN KEY (user_id)
        REFERENCES users (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE reviews
    ADD CONSTRAINT FK_reviews_product_id_products_id FOREIGN KEY (product_id)
        REFERENCES products (id) ON DELETE RESTRICT ON UPDATE RESTRICT;
        
ALTER TABLE reviews
    ADD CONSTRAINT FK_reviews_wearing_sensation_id FOREIGN KEY (wearing_sensation_id)
        REFERENCES wearing_sensations (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

CREATE TABLE question_types
(
    `id`    INT            NOT NULL    AUTO_INCREMENT COMMENT '아이디', 
    `name`  VARCHAR(64)    NOT NULL    COMMENT '유형 이름', 
    PRIMARY KEY (id)
);

ALTER TABLE question_types COMMENT '문의유형';

CREATE TABLE question_tables
(
    `id`                INT         NOT NULL    AUTO_INCREMENT COMMENT '아이디', 
    `product_id`        INT         NOT NULL    COMMENT '상품 아이디', 
    `register_date`     DATETIME    NOT NULL    DEFAULT NOW() COMMENT '등록일', 
    `user_id`           INT         NOT NULL    COMMENT '유저 아이디', 
    `question_content`  TEXT        NOT NULL    COMMENT '문의 내용', 
    `question_type_id`  INT         NOT NULL    COMMENT '문의 유형 아이디', 
    `updated_at`        DATETIME    NOT NULL    COMMENT '수정일자',
    `is_deleted`        TINYINT     NOT NULL    COMMENT '삭제 여부', 
    PRIMARY KEY (id)
);

ALTER TABLE question_tables
    ADD CONSTRAINT FK_question_tables_product_id_products_id FOREIGN KEY (product_id)
        REFERENCES products (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE question_tables
    ADD CONSTRAINT FK_question_tables_user_id_users_id FOREIGN KEY (user_id)
        REFERENCES users (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE question_tables
    ADD CONSTRAINT FK_question_tables_question_type_id_question_types_id FOREIGN KEY (question_type_id)
        REFERENCES question_types (id) ON DELETE RESTRICT ON UPDATE RESTRICT;


-- orders Table Create SQL
CREATE TABLE orders
(
    `id`                      INT             NOT NULL    AUTO_INCREMENT, 
    `order_number`            VARCHAR(128)    NOT NULL, 
    `final_price`             INT             NOT NULL, 
    `order_date`              DATETIME        NOT NULL    DEFAULT NOW(), 
    `user_id`                 INT             NOT NULL,
    `shipping_infomation_id`  INT             NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE orders
    ADD CONSTRAINT FK_order_user_id FOREIGN KEY (user_id)
        REFERENCES users (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE orders
    ADD CONSTRAINT FK_orders_shipping_infomation_id FOREIGN KEY (shipping_infomation_id)
        REFERENCES shipping_informations (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- order_cancel_reasons Table Create SQL

CREATE TABLE order_cancel_reasons
(
    `id`    INT            NOT NULL    AUTO_INCREMENT, 
    `name`  VARCHAR(64)    NOT NULL, 
    PRIMARY KEY (id)
);

-- order_refund_reasons Table Create SQL

CREATE TABLE order_refund_reasons
(
    `id`    INT            NOT NULL    AUTO_INCREMENT,
    `name`  VARCHAR(64)    NOT NULL,
    PRIMARY KEY (id)
);

-- order_details Table Create SQL
CREATE TABLE order_details
(
    `id`                               INT             NOT NULL    AUTO_INCREMENT, 
    `order_id`                         INT             NOT NULL, 
    `order_detail_number`              VARCHAR(128)    NOT NULL, 
    `order_detail_statuses_id`         INT             NOT NULL, 
    `option_id`                        INT             NOT NULL, 
    `quantity`                         INT             NOT NULL, 
    `price`                            INT             NOT NULL, 
    `is_comfirmed`                     TINYINT(1)      NOT NULL, 
    `order_cancel_reason_id`           INT             NULL, 
    `order_refund_reason_id`           INT             NULL, 
    `order_refund_reason_description`  TEXT            NULL, 
    `coupon_id`                        INT             NULL, 
    `discount_price`                   INT             NULL        DEFAULT 0, 
    `final_price`                      INT             NOT NULL, 
    PRIMARY KEY (id)
);

ALTER TABLE order_details
    ADD CONSTRAINT FK_order_details_cancel_reason_id FOREIGN KEY (order_cancel_reason_id)
        REFERENCES order_cancel_reasons (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE order_details
    ADD CONSTRAINT FK_order_details_refund_reason_id FOREIGN KEY (order_refund_reason_id)
        REFERENCES order_refund_reasons (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE order_details
    ADD CONSTRAINT FK_order_details_option_id FOREIGN KEY (option_id)
        REFERENCES options (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE order_details
    ADD CONSTRAINT FK_order_details_coupon_id FOREIGN KEY (coupon_id)
        REFERENCES coupons (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE order_details
    ADD CONSTRAINT FK_order_id FOREIGN KEY (order_id)
        REFERENCES orders (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

-- order_statuses Table Create SQL
CREATE TABLE order_statuses
(
    `id`    INT            NOT NULL    AUTO_INCREMENT, 
    `name`  VARCHAR(64)    NOT NULL, 
    PRIMARY KEY (id)
);

-- second_categories Table Create SQL
CREATE TABLE order_status_modification_histories
(
    `id`               INT         NOT NULL    AUTO_INCREMENT,
    `order_detail_id`  INT         NOT NULL,
    `updated_at`       DATETIME    NOT NULL    DEFAULT NOW(),
    `order_status_id`  INT         NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE order_status_modification_histories
    ADD CONSTRAINT FK_order_detail_id FOREIGN KEY (order_detail_id)
        REFERENCES order_details (id) ON DELETE RESTRICT ON UPDATE RESTRICT;

ALTER TABLE order_status_modification_histories
    ADD CONSTRAINT FK_order_status_id FOREIGN KEY (order_status_id)
        REFERENCES order_statuses (id) ON DELETE RESTRICT ON UPDATE RESTRICT;