-- DROP DATABASE IF EXISTS brandi;
-- CREATE DATABASE brandi;
USE brandi;

# 은행 테이블
INSERT INTO banks
VALUES (1,'한국은행'),(2,'산업은행'),(3,'기업은행'),(4,'국민은행'),(5,'수협중앙회'),
(6,'수출입은행'),(7,'농협중앙회'),(8,'지역 농축협'),(9,'우리은행'),(10,'SC은행'),
(11,'한국씨티은행'),(12,'대구은행'),(13,'부산은행'),(14,'광주은행'),(15,'제주은행'),
(16,'전북은행'),(17,'경남은행'),(18,'새마을금고중앙회'),(19,'신협중앙회'),(20,'상호저축은행');

#3.seller_properties(셀러 속성 테이블)
INSERT INTO seller_properties (`id`, `name`)
VALUES (1, '쇼핑몰'), (2, '마켓'), (3, '로드샵'), 
(4, '디자이너브랜드'), (5, '제너럴브랜드'), (6, '내셔널브랜드'), (7, '뷰티');

#4.seller_statuses(셀러 상태 테이블)
INSERT INTO seller_statuses VALUES (1,'입점대기'),(2,'입점거절'),(3,'입점'),(4,'휴점'),(5,'퇴점 대기'),(6,'퇴점');

#5.sellers
INSERT INTO sellers(
    `register_date`,
    `is_deleted`
)VALUES (
    NOW(),
    False
);

#6.seller_informations
-- password : hellow1234
INSERT INTO seller_informations (
    `id`,
    `seller_id`,
    `seller_status_id`,
    `is_master`,
    `seller_account`,
    `english_name`,
    `korean_name`,
    `cs_phone`,
    `seller_property_id`,
    `profile_image`,
    `password`,
    `background_image`,
    `simple_description`,
    `detail_description`,
    `zip_code`,
    `address`,
    `detail_address`,
    `open_time`,
    `close_time`,
    `bank_id`,
    `account_number`,
    `account_name`,
    `shipping_information`,
    `exchange_refund_information`,
    `model_height`,
    `model_top_size`,
    `model_bottom_size`,
    `model_feet_size`,
    `shopping_feedtext`,
    `registered_product_count`,
    `created_at`,
    `expired_at`
) VALUES (
    1,
    1,
    1,
	False,
    'seller1',
    'leejiyeon1',
	'이지연1',
	'02-123-4500',
    1,
    'https://image.brandi.me/cproduct/2020/01/17/13216968_1579243036_image1_L.jpg',
	'$2b$12$4G24HQNaMQcGxPaZjl5fce30INJUXcgwGp3VZDsa/ZTLUc8Ff7GzS', 
    'https://image.brandi.me/cproduct/2020/01/17/13216968_1579243036_image1_L.jpg',
    '안녕하세요1',
	'안녕하세요.상세페이지입니다1',
    '041-300',
	'서울특별시 강남구 테헤란로 32길 263 청송빌딩',
	'역삼 브랜디',
	'10:00',
    '18:00',
    1,                              
    '02-45940301-226433',
    '이지연',
	'도서산간 지역은 배송비가 추가비용이 발생할 수 있으며, 그 외 지역은 무료배송입니다.',
	'브랜디는 소비자보호법 및 전자상거래법을 기반한 환불보장제를 운영 중에 있습니다.',
	'170',
	'55',
	'55',
	'245',
	'안녕하세요! 가을에 어울리는 신상이 100개 입고되었습니다.',
    0,
    now(),
    '9999-12-31 23:59:59'
);

-- 셀러 상태 변경 이력 테이블 
-- INSERT INTO seller_status_modification_histories (
--     `id`,
--     `seller_id`, 
--     `updated_at`, 
--     `seller_status_id`, 
--     `modifier_id`
-- )
-- VALUES('1', '1', now(), '1', '1');

-- 셀러 담당자 테이블
INSERT INTO seller_managers (`id`, `name`, `phone_number`, `email`, `seller_id`)
VALUES (
    1,
    '홍길동',
    '010-4882-9413',
    'seller_manager1@google.com',
    1
);


INSERT INTO first_categories (`id`, `name`) 
VALUES (1, '아우터'), (2, '상의'), (3, '바지'), (4, '원피스'), (5, '스커트'), (6, '신발'), (7, '가방'), (8, '주얼리'), (9, '잡화'), (10, '라이프웨어'), (11, '빅사이즈'), 
(12, '아우터'), (13, '상의'), (14, '바지'), (15, '원피스'), (16, '스커트'), (17, '신발'), (18, '가방'), (19, '주얼리'), (20, '잡화'), (21, '라이프웨어'), (22, '스포츠웨어'), 
(23, '스킨케어'), (24, '메이크업'), (25, '바디케어'), (26, '헤어케어'), (27, '향수'), (28, '미용소품');

INSERT INTO first_category_seller_properties (`seller_property_id`, `first_category_id`)
VALUES (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10), (1, 11), 
(2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6), (2, 7), (2, 8), (2, 9), (2, 10), (2, 11), 
(3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8), (3, 9), (3, 10), (3, 11), 
(4, 12), (4, 13), (4, 14), (4, 15), (4, 16), (4, 17), (4, 18), (4, 19), (4, 20), (4, 21), (4, 22),
(5, 12), (5, 13), (5, 14), (5, 15), (5, 16), (5, 17), (5, 18), (5, 19), (5, 20), (5, 21), (5, 22),
(6, 12), (6, 13), (6, 14), (6, 15), (6, 16), (6, 17), (6, 18), (6, 19), (6, 20), (6, 21), (6, 22),
(7, 23), (7, 24), (7, 25), (7, 26), (7, 27);

INSERT INTO second_categories (`id`, `name`)
VALUES (1, '자켓'), (2, '가디건'), (3, '코트'), (4, '점퍼'), (5, '패딩'), (6, '무스탕/퍼'), (7, '기타'), 
(8, '티셔츠'), (9, '셔츠/블라우스'), (10, '니트'), (11, '후드/맨투맨'), (12, '베스트'), 
(13, '청바지'), (14, '슬랙스'), (15, '면바지'), (16, '반바지'), (17, '트레이닝/조거'), (18, '레깅스'),
(19, '미니'), (20, '미디'), (21, '롱'), (22, '투피스'), (23, '점프수트'),
(24, '미니'), (25, '미디'), (26, '롱'),
(27, '플랫/로퍼'), (28, '샌들/슬리퍼'), (29, '힐'), (30, '스니커즈'), (31, '부츠/워커'),
(32, '크로스백'), (33, '토트백'), (34, '숄더백'), (35, '에코백'), (36, '클러치'), (37, '백팩'),
(38, '귀걸이'), (39, '목걸이'), (40, '팔찌/발찌'), (41, '반지'),
(42,'휴대폰 acc'), (43, '헤어 acc'), (44, '양말/스타킹'), (45, '지갑/파우치'), (46, '모자'), (47, '벨트'), (48, '시계'), (49, '스카프/머플러'), (50, '아이웨어'), (51, '기타'),
(52, '언더웨어'), (53, '홈웨어'), (54, '스웜웨어'), (55, '비치웨어'), (56, '기타'),
(57, '아우터'), (58, '상의'), (59, '바지'), (60, '원피스'), (61, '스커트'),
(62, '코트'), (63, '점퍼'), (64, '자켓'), (65, '가디건'), (66, '기타'),
(67, '티/반팔티'), (68, '민소매/나시'), (69, '셔츠/블라우스'), (70, '니트'), (71, '맨투맨'), (72, '후드/집업'), (73, '기타'), 
(74, '청바지'), (75, '면바지'), (76, '슬랙스'), (77, '반바지'), (78, '트레이닝/조거'), (79, '기타'),
(80, '미니'), (81, '미디'), (82, '롱'), (83, '점프수트'), (84, '기타'),
(85, '미니'), (86, '미디'), (87, '롱'), (88, '기타'),
(89, '스니커즈'), (90, '러닝화'), (91, '플랫/로퍼'), (92, '펌프스'), (93, '부츠'), (94, '샌들/슬리퍼'), (95, '기타'),
(96, '숄더백'), (97, '토트백'), (98, '에코백'), (99, '백팩'), (100, '지갑/파우치'), (101, '클러치'), (102, '기타'),
(103, '귀걸이'), (104, '목걸이'), (105, '반지'),(106, '팔찌/발찌'),
(107, '시계'), (108, '스카프/머플러'), (109, '모자'), (110, '양말'), (111, '폰 악세서리'), (112, '선글라스/아이웨어'), (113, '기타'),
(114, '언더웨어'), (115, '홈웨어'),
(116, '상의'), (117, '하의'), (118, '레깅스'), (119, '스웜웨어'), (120, '기타'),
(121, '스킨/토너'), (122, '에센스/앰플'), (123, '크림'), (124, '클렌징'), (125, '기타'),
(126, '베이스'), (127, '립'), (128, '아이'),
(129, '로션/크림'), (130, '워시/스크럽'), 
(131, '샴푸/린스'), (132, '트리트먼트'), (133, '스타일링/에센스'),
(134, '향수'), (135, '디퓨저/방향제'),
(136, '뷰티툴'), (137, '네일'), (138, '기타');

INSERT INTO first_category_second_categories (`id`, `first_category_id`, `second_category_id`)
VALUES (1, 1, 1), (2, 1, 2), (3, 1, 3), (4, 1, 4), (5, 1, 5), (6, 1, 6), (7, 1, 7),
(8, 2, 8), (9, 2, 9), (10, 2, 10), (11, 2, 11), (12, 2, 12),
(13, 3, 13), (14, 3, 14), (15, 3, 15), (16, 3, 16), (17, 3, 17), (18, 3, 18),
(19, 4, 19), (20, 4, 20),(21, 4, 21), (22, 4, 22), (23, 4, 23),
(24, 5, 24), (25, 5, 25), (26, 5, 26),
(27, 6, 27), (28, 6, 28), (29, 6, 29), (30, 6, 30), (31, 6, 31),
(32, 7, 32), (33, 7, 33), (34, 7, 34), (35, 7, 35), (36, 7, 36), (37, 7, 37), 
(38, 8, 38), (39, 8, 39), (40, 8, 40), (41, 8, 41), 
(42, 9, 42), (43, 9, 43), (44, 9, 44), (45, 9, 45), (46, 9, 46), (47, 9, 47), (48, 9, 48), (49, 9, 49), (50, 9, 50), (51, 9, 51),
(52, 10, 52), (53, 10, 53), (54, 10, 54), (55, 10, 55), (56, 10, 56),
(57, 11, 57), (58, 11, 58), (59, 11, 59), (60, 11, 60), (61, 11, 61), 
(62, 12, 62), (63, 12, 63), (64, 12, 64), (65, 12, 65), (66, 12, 66), 
(67, 13, 67), (68, 13, 68), (69, 13, 69), (70, 13, 70), (71, 13, 71), (72, 13, 72), (73, 13, 73), 
(74, 14, 74), (75, 14, 75), (76, 14, 76), (77, 14, 77), (78, 14, 78), (79, 14, 79), 
(80, 15, 80), (81, 15, 81), (82, 15, 82), (83, 15, 83), (84, 15, 84), 
(85, 16, 85), (86, 16, 86), (87, 16, 87), (88, 16, 88),
(89, 17, 89), (90, 17, 90), (91, 17, 91), (92, 17, 92), (93, 17, 93), (94, 17, 94), (95, 17, 95),
(96, 18, 96), (97, 18, 97), (98, 18, 98), (99, 18, 99), (100, 18, 100), (101, 18, 101), (102, 18, 102),
(103, 19, 103), (104, 19, 104), (105, 19, 105), (106, 19, 106),
(107, 20, 107), (108, 20, 108), (109, 20, 109), (110, 20, 110), (111, 20, 111), (112, 20, 112), (113, 20, 113),
(114, 21, 114), (115, 21, 115),
(116, 22, 116), (117, 22, 117), (118, 22, 118), (119, 22, 119), (120, 22, 120),
(121, 23, 121), (122, 23, 122), (123, 23, 123), (124, 23, 124), (125, 23, 125),
(126, 24, 126), (127, 24, 127), (128, 24, 128),
(129, 25, 129), (130, 25, 130),
(131, 26, 131), (132, 26, 132), (133, 26, 133),
(134, 27, 134), (135, 27, 135),
(136, 28, 136), (137, 28, 137), (138, 28, 138);

INSERT INTO country_of_origins (`id`, `name`)
VALUES (1, '한국'), (2, '중국'), (3, '베트남'), (4, '기타');

INSERT INTO colors (`id`, `name`)
VALUES (1, 'Black'), (2, 'White'), (3, 'Gray'), (4, 'Ivory'), (5, 'Navy'), (6, 'Brown'), (7, 'Wine');

INSERT INTO sizes (`id`, `name`)
VALUES (1, 'Free'), (2, 'XL'), (3, 'L'), (4, 'M'), (5, 'S'), (6, 'XS');

-- 상품
INSERT INTO products (`id`, `sale_amount`, `code`, `seller_id`, `categories_id`, `qna_count`)
VALUES (1, 300, 'e8a468df-7979-4c20-986d-b54486ce6bba', 1, 1, 1);

-- 상품 옵션
INSERT INTO options (
	`id`,
	`stock`,
	`product_id`,
    `color_id`,
	`size_id`
) VALUES (1,1,1,3,1), (2,0,1,2,1), (0,1,1,1,1);

INSERT INTO product_details (
	`id`,
	`name`,                 
    `origin_company`,
    `origin_date`,
    `simple_description`,
    `description`,
    `sale_price`,
    `discount_rate`,
    `discount_started_at`,
    `discount_ended_at`,
    `minimum_sale_amount`,
    `maximum_sale_amount`, 
    `modifier_id`,
    `product_id`,
    `country_of_origin_id`)
VALUES (
	1,
	'로이드 린넨노카라반팔자켓',
    null,
    null,
    null,
    "<img src='http://beginning1.img10.kr/begin/sa/begin/120.jpg' /><br /><p style='text-align:center'><strong>로이드 린넨노카라반팔자켓</strong></p><br /><br /><br /><br />어깨에 패드가 들어가 탄탄한 핏을 잡아주고<br />노카라넥으로 깔끔해 보이며,<br />이너 포인트 주기 좋은 자켓이에요.<br /><br />비비드 한 컬러감이 돋보이며,<br />스탠다드하게 툭 떨어지는 실루엣이 멋스러워요,<br />힙을 살짝 덮는 기장감으로 안정감이 느껴지고<br />양 사이드포켓으로 실용성까지 더해준 제품이에요.<br /><br />소매기장도 짧지 않고 적당해 팔뚝 라인을 감춰주며,<br />린넨 혼방 소재로 쾌적한 착용감까지 느끼게 해줘<br />한여름까지 즐기기 좋아요.<br /><br /><br /><br /><br /> <div><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_22.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_9.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_10.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_11.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_12.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_13.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_14.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_1.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_2.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_3.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_4.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_5.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_6.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_7.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_8.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_15.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_16.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_17.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_18.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_19.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_20.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_21.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060401/1_23.jpg' /><br /><img src='http://beginning1.img10.kr/begin/b/beginning/220.jpg' /><div><br /><img src='http://beginning1.img10.kr/begin/a/begin/detail_notice.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060403/2_01.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060403/2_02.jpg' /><br /><img src='http://beginning1.img10.kr/begin/sa/begin/120.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060403/2_03.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060403/2_04.jpg' /><br /><img src='http://beginning1.img10.kr/begin/sa/begin/120.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060403/2_05.jpg' /><br /><img src='http://beginning1.img10.kr/begin/sa/begin/120.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060403/2_06.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060403/2_07.jpg' /><br /><img src='http://beginning1.img10.kr/begin/sa/begin/120.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060403/2_08.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060403/2_09.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060403/2_10.jpg' /><br /><br /><br /><img src='http://beginning1.img10.kr/begin/sa/begin/191108/wash_01.jpg' /><br /><img src='http://beginning1.img10.kr/begin/sa/begin/191108/wash_rayon2.jpg' /><br /><br /><br /><br /><img src='http://beginning1.img10.kr/begin/h/begin/linen01.jpg' /><br /> <div><br /><img src='http://beginning1.img10.kr/begin/i/20060403/0_01.jpg' /><br /><img src='http://beginning1.img10.kr/begin/i/20060403/00_02.jpg' /><br /><br /><strong>원산지</strong> : KOREA<br /><strong>제조사</strong> : 비기닝리테일(주) 협력업체<br /><strong>제조년월</strong> : 2020.06<br /><strong>A/S 정보 및 담당자 </strong> : 비기닝리테일(주) 고객센터 / 1599-2219<br /><strong>품질보증기준</strong> : 전자상거래 소비자 보호법에 규정되어 있는<br />소비자 청약철회 가능범위를 준수합니다.<br /><br /><br /><br /> </div></div></div><br /><img src='http://beginning1.img10.kr/begin/a/begin/profile11.jpg' /><br /><img src='http://beginning1.img10.kr/begin/11st/washingtip_%BF%DC%BA%CE%C3%A4%B3%CE.jpg' />",
    59000,
    30,
    NOW(),
    '2020-11-11 00:00:00',
    1,
    20,
    1,
    1,
    null
);

INSERT INTO product_images(
    id,
    product_id,
    image_path,
    ordering
) VALUES (
    1,
    1,
    'https://wecode11-brandi.s3.ap-northeast-2.amazonaws.com/e8a468df-7979-4c20-986d-b54486ce6bba_roid_1.jpg',
    1
), (
    2,
    1,
    'https://wecode11-brandi.s3.ap-northeast-2.amazonaws.com/e8a468df-7979-4c20-986d-b54486ce6bba_roid_2.jpg',
    2
);

INSERT INTO users(register_date,is_deleted) VALUES('2020-10-01 12:30:50',0);

INSERT INTO user_informations(user_id,account_id,name,email,phone_number,password,modifier_id,created_at,expired_at) VALUES(1,'tester001','보라돌이','tester001@gmail.com','010-0001-0001','$2b$12$9eALKlmxb8jcZlRW94TvCOXlCKuKSgnzT7q86bBY6H7IXwDj7.QjK',NULL,'2020-10-01 12:30:50','9999-12-31 00:00:00');

INSERT INTO wearing_sensations (content) VALUES ('너무 커요'),
('조금 커요'),('잘 맞아요'),('조금 작아요'),('많이 작아요');

INSERT INTO reviews (
    user_id,
    product_id,
    content,
    register_date,
    updated_at,
    grade,
    is_deleted,
    modifier_id,
    option_text,
    wearing_sensation_id,
    height,
    top,
    bottom,
    shoe_size
) VALUES (
    1,
    1,
    '많이 파세요', 
    '2020-10-20 12:30:50',
    NULL,
    1,
    0,
    NULL,
    '블랙/L',
    1,
    162,
    55,
    55,
    '240mm'
);

INSERT INTO shipping_informations (name,phone_number,user_id,is_default_address,zip_code,address,detail_address,is_deleted) VALUES ('스펀지밥','010-1111-2222',1,1,12345,'비키니시티 깊은 저 바다속','파인애플',0);

INSERT INTO question_types (name) VALUES ('상품문의'),('조회/반품'),('불량/오배송'),
('기타'),('배송문의'),('하루배송'),('취소/변경');

INSERT INTO questions (
    product_id,
    created_at,
    user_id,
    question_content,
    question_type_id,
    updated_at,
    is_deleted,
    is_answered,
    is_secreted
) VALUES (
        1,
        NOW(),
        1,
        '대체 언제 배송 되나요?',
        1,
        NULL,
        0,
        0,
        0
);

INSERT INTO order_cancel_reasons
(name) VALUES ('구매자 취소'), ('구매자 변심'), ('상품 품절');

INSERT INTO order_refund_reasons
(name) VALUES ('단순 변심'), ('상품 불량'), ('오배송'), ('교환요청'), ('일부상품누락'), ('기타');

INSERT INTO order_statuses
(name) VALUES ('결제완료'), ('상품준비'), ('배송중'), ('배송완료'), ('구매확정'), ('주문취소완료'), ('환불요청'), ('환불완료');

INSERT INTO coupon_issues (id, name)
VALUES (1, '일반'), (2, '쿠폰코드'), (3, '시리얼번호');

INSERT INTO coupon_types (id, name)
VALUES (1, '상품 할인 쿠폰');

INSERT INTO coupons (id, is_deleted)
VALUES (1,0), (2,0), (3,0), (4,0);

INSERT INTO coupon_details (
	coupon_id,
    name,
    coupon_type_id,
    is_downloadable,
    coupon_issue_id,
    coupon_code,
    description,
    download_started_at,
    download_ended_at,
    valid_started_at,
    valid_ended_at,
    discount_price,
    limit_count,
    minimum_price,
    download_count,
    use_count,
    updated_at,
    modifier_id
) VALUES (1, '브랜디 감사대전 3000원 할인쿠폰', 1, 1, 1, NULL, '브랜디 감사대전 이벤트 쿠폰입니다.', 
	'2020-10-06 00:00:00', '2020-11-05 23:59:59',
    '2020-10-06 00:00:10', '2020-11-30 23:59:59',
    3000, NULL, 20000, 0, 0, NOW(), 1
),
(2, '브랜디 감사대전 10000원 할인쿠폰', 1, 1, 1, NULL, '브랜디 감사대전 이벤트 쿠폰입니다.', 
	'2020-10-06 00:00:00', '2020-11-05 23:59:59',
    '2020-10-06 00:00:10', '2020-11-30 23:59:59',
    10000, NULL, 50000, 0, 0, NOW(), 1
),
(3, '브랜디 감사대전 20000원 할인쿠폰', 1, 1, 1, NULL, '브랜디 감사대전 이벤트 쿠폰입니다.', 
	'2020-10-06 00:00:00', '2020-11-05 23:59:59',
    '2020-10-06 00:00:10', '2020-11-30 23:59:59',
    20000, NULL, 100000, 0, 0, NOW(), 1
),
(4, '빼빼로데이 기념 쿠폰', 1, 1, 1, NULL, '빼빼로데이를 기념하는 할인 쿠폰입니다.', 
	'2020-11-11 00:00:00', '2020-11-11 23:59:59',
    '2020-11-11 00:00:00', '2020-11-22 23:59:59',
    5000, NULL, 30000, 0, 0, NOW(), 1
);

INSERT INTO event_types (name)
VALUES ('이벤트'), ('쿠폰'), ('상품(이미지)'), ('상품(텍스트)'), ('유튜브');

INSERT INTO event_statuses (name)
VALUES ('진행중'), ('종료'), ('대기');

INSERT INTO event_button_link_types (name)
VALUES ('GNB 홈 - tab 홈'), ('GNB 홈 - tab 베스트'), ('GNB 홈 - tab 쇼핑몰*마켓'), ('GNB 홈 - tab 브랜드'), ('GNB 홈 - tab 뷰티'), ('GNB 홈 - 특가'), ('GNB 홈 - tab 기획전'), ('GNB 마이'), ('GNB 스토어 - 쇼핑몰*마켓'), ('GNB 스토어 - 브랜드'), ('GNB 스토어 - 뷰티'), ('Pg 카테고리 - 쇼핑몰*마켓'), ('Pg 카테고리 - 브랜드'), ('Pg 카테고리 - 뷰티'), ('Pg 상품상세'), ('Pg 스토어상세 - 스토어'), ('Pg 이벤트 상세'), ('Pg 포인트'), ('Pg 쿠폰'), ('Pg 친구초대'), ('Pg 하루배송'), ('웹링크(웹뷰)'), ('웹링크(외부)'), ('쿠폰다운로드');

INSERT INTO event_kinds (name, event_type_id)
VALUES ('댓글창 있음', 1), ('댓글창 없음', 2), ('상품', 3), ('버튼', 3), ('상품', 4), ('버튼', 4), ('상품', 5), ('버튼', 5);
