-- also see http://android.choosemuse.com/enumcom_1_1choosemuse_1_1libmuse_1_1_muse_data_packet_type.html

CREATE DATABASE IF NOT EXISTS muse;
USE muse;

CREATE TABLE IF NOT EXISTS subjects (id INT PRIMARY KEY AUTO_INCREMENT, first_name VARCHAR(255), last_name VARCHAR(255), birthday DATE, gender VARCHAR(255), race VARCHAR(255), occupation VARCHAR(255));

-- http://ios.choosemuse.com/_i_x_n_eeg_8h.html
-- IXNEegEEG1      Left ear
-- IXNEegEEG2      Left forehead
-- IXNEegEEG3      Right forehead
-- IXNEegEEG4      Right ear 
-- IXNEegAUXLEFT   Left auxiliary.
-- IXNEegAUXRIGHT  Right auxiliary.
CREATE TABLE IF NOT EXISTS raw (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, eeg1 FLOAT, eeg2 FLOAT, eeg3 FLOAT, eeg4 FLOAT, aux1 FLOAT, aux2 FLOAT); -- raw EEG data
CREATE TABLE IF NOT EXISTS alpha (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, eeg1 FLOAT, eeg2 FLOAT, eeg3 FLOAT, eeg4 FLOAT, aux1 FLOAT, aux2 FLOAT); -- absolute alpha power
CREATE TABLE IF NOT EXISTS beta (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, eeg1 FLOAT, eeg2 FLOAT, eeg3 FLOAT, eeg4 FLOAT, aux1 FLOAT, aux2 FLOAT); -- absolute beta power
CREATE TABLE IF NOT EXISTS delta (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, eeg1 FLOAT, eeg2 FLOAT, eeg3 FLOAT, eeg4 FLOAT, aux1 FLOAT, aux2 FLOAT); -- absolute delta power
CREATE TABLE IF NOT EXISTS theta (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, eeg1 FLOAT, eeg2 FLOAT, eeg3 FLOAT, eeg4 FLOAT, aux1 FLOAT, aux2 FLOAT); -- absolute theta power
CREATE TABLE IF NOT EXISTS gamma (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, eeg1 FLOAT, eeg2 FLOAT, eeg3 FLOAT, eeg4 FLOAT, aux1 FLOAT, aux2 FLOAT); -- absolute gamma power
CREATE TABLE IF NOT EXISTS good (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, eeg1 FLOAT, eeg2 FLOAT, eeg3 FLOAT, eeg4 FLOAT, aux1 FLOAT, aux2 FLOAT); -- is channel quality good?

-- http://ios.choosemuse.com/_i_x_n_accelerometer_8h.html
CREATE TABLE IF NOT EXISTS accelerometer (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, x FLOAT, y FLOAT, z FLOAT, fb FLOAT, ud FLOAT, lr FLOAT);
-- http://ios.choosemuse.com/_i_x_n_gyro_8h.html
CREATE TABLE IF NOT EXISTS gyro (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, x FLOAT, y FLOAT, z FLOAT, fb FLOAT, ud FLOAT, lr FLOAT);

-- http://ios.choosemuse.com/_i_x_n_muse_artifact_packet_8h_source.html
CREATE TABLE IF NOT EXISTS artifact (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, headband BOOLEAN, blink BOOLEAN, jaw BOOLEAN);
