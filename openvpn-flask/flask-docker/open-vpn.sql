/*
 
 Date: 08/05/2020 17:01:17
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
create database `open-vpn`;
use    `open-vpn` ;
-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin`  (
  `admin_id` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `admin_pass` varchar(80) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`admin_id`) USING BTREE,
  UNIQUE INDEX `admin_pass`(`admin_pass`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES ('admin', '123456');

-- ----------------------------
-- Table structure for log
-- ----------------------------
DROP TABLE IF EXISTS `log`;
CREATE TABLE `log`  (
  `log_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `log_trusted_ip` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `log_trusted_port` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `log_remote_ip` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `log_remote_port` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `log_start_time` datetime(0) NULL DEFAULT NULL,
  `log_end_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`log_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 14 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of log
-- ----------------------------
INSERT INTO `log` VALUES (1, 'qeqwreqw', '192.178.11.33', '290', '192.33.145.135', '900', '2020-05-07 22:46:03', '2020-05-25 22:46:09');
INSERT INTO `log` VALUES (2, '3154', '193.118.32.11', '8888', '193.56.141.11', '838', '2020-05-05 22:47:30', '2020-05-19 22:47:33');
INSERT INTO `log` VALUES (3, 'test', '172.20.7.136', '50463', '10.8.0.6', '1194', '2020-05-04 18:50:46', '2020-05-04 18:54:46');
INSERT INTO `log` VALUES (7, 'test', '172.20.7.136', '53313', '10.8.0.6', '1194', '2020-05-04 19:14:08', '2020-05-04 19:14:24');
INSERT INTO `log` VALUES (8, 'test', '192.168.0.190', '44241', '10.8.0.6', '1194', '2020-05-06 09:32:56', '2020-05-06 09:43:59');
INSERT INTO `log` VALUES (9, 'test', '192.168.0.190', '41807', '10.8.0.6', '1194', '2020-05-06 09:43:59', '2020-05-06 10:01:21');
INSERT INTO `log` VALUES (10, 'test', '192.168.0.190', '48143', '10.8.0.6', '1194', '2020-05-06 10:01:24', '2020-05-06 10:49:49');
INSERT INTO `log` VALUES (11, 'test', '192.168.0.190', '42583', '10.8.0.6', '1194', '2020-05-06 10:49:49', '2020-05-06 17:12:40');
INSERT INTO `log` VALUES (12, 'test', '192.168.0.191', '2435', '10.8.0.6', '1194', '2020-05-08 14:40:33', '2020-05-08 14:40:37');
INSERT INTO `log` VALUES (13, 'te2345', '192.168.0.193', '2422', '10.8.0.8', '1133', '2020-05-08 14:41:32', '2020-05-08 14:41:36');

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `user_id` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `user_pass` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `user_online` tinyint(1) NULL DEFAULT NULL,
  `user_enable` tinyint(1) NULL DEFAULT NULL,
  `user_start_date` datetime(0) NULL DEFAULT NULL,
  `user_end_date` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES ('asav', 'wdfsb44', NULL, NULL, '2020-05-01 00:00:00', '2020-05-07 00:00:00');
INSERT INTO `user` VALUES ('dat', '123456', 0, 1, '2020-05-01 00:00:00', '2020-05-04 00:00:00');
INSERT INTO `user` VALUES ('erdan', '123456', 1, 1, '2020-05-08 16:53:20', NULL);
INSERT INTO `user` VALUES ('fucku', '123456', 1, 1, '2020-05-08 16:53:20', NULL);
INSERT INTO `user` VALUES ('gf', '123456', 1, 1, '2020-05-21 00:00:00', '2020-05-21 00:00:00');
INSERT INTO `user` VALUES ('lisi', '123456', 1, 1, '2020-05-08 16:52:43', NULL);
INSERT INTO `user` VALUES ('ll', '12234', 1, 0, '2020-05-05 00:00:00', '2020-05-06 00:00:00');
INSERT INTO `user` VALUES ('sb', '123456', 1, 1, '2020-05-08 16:53:20', NULL);
INSERT INTO `user` VALUES ('sjhh', '123456', 1, 1, '2020-05-04 00:00:00', '2020-05-05 00:00:00');
INSERT INTO `user` VALUES ('test', '123456', 0, 1, NULL, NULL);
INSERT INTO `user` VALUES ('wanger', '123456', 1, 1, '2020-05-08 16:59:17', NULL);
INSERT INTO `user` VALUES ('zhangsan', '123456', 1, 1, '2020-05-08 16:52:08', NULL);
INSERT INTO `user` VALUES ('zrrr', '123456', 0, 1, '2020-05-01 00:00:00', '2020-05-13 00:00:00');
INSERT INTO `user` VALUES ('zz', '123456', 1, 1, '2020-05-08 00:00:00', NULL);
INSERT INTO `user` VALUES ('zzz', '123456', 0, 1, '2020-05-07 00:00:00', '2020-05-09 00:00:00');

SET FOREIGN_KEY_CHECKS = 1;
