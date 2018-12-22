-- Muse available data -- see http://developer.choosemuse.com/tools/available-data
--

CREATE DATABASE IF NOT EXISTS muse;
USE muse;

CREATE TABLE IF NOT EXISTS subjects (id INT PRIMARY KEY AUTO_INCREMENT, first_name VARCHAR(255), last_name VARCHAR(255), birthday DATE, gender VARCHAR(255), race VARCHAR(255), occupation VARCHAR(255));

-- 6 channels:
-- http://ios.choosemuse.com/_i_x_n_eeg_8h.html
--    IXNEegEEG1      Left ear
--    IXNEegEEG2      Left forehead
--    IXNEegEEG3      Right forehead
--    IXNEegEEG4      Right ear 
--    IXNEegAUXLEFT   Left auxiliary.
--    IXNEegAUXRIGHT  Right auxiliary.
-- also see http://android.choosemuse.com/enumcom_1_1choosemuse_1_1libmuse_1_1_muse_data_packet_type.html#a6723edfb11680ad66941b0ea4b86ed4c
CREATE TABLE IF NOT EXISTS raw (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, utimestamp BIGINT, eeg1 FLOAT, eeg2 FLOAT, eeg3 FLOAT, eeg4 FLOAT, aux1 FLOAT, aux2 FLOAT); -- IXNMuseDataPacketTypeEeg
CREATE TABLE IF NOT EXISTS alpha (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, utimestamp BIGINT, eeg1 FLOAT, eeg2 FLOAT, eeg3 FLOAT, eeg4 FLOAT, aux1 FLOAT, aux2 FLOAT); -- IXNMuseDataPacketTypeAlphaAbsolute
CREATE TABLE IF NOT EXISTS beta (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, utimestamp BIGINT, eeg1 FLOAT, eeg2 FLOAT, eeg3 FLOAT, eeg4 FLOAT, aux1 FLOAT, aux2 FLOAT); -- IXNMuseDataPacketTypeBetaAbsolute
CREATE TABLE IF NOT EXISTS delta (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, utimestamp BIGINT, eeg1 FLOAT, eeg2 FLOAT, eeg3 FLOAT, eeg4 FLOAT, aux1 FLOAT, aux2 FLOAT); -- IXNMuseDataPacketTypeDeltaAbsolute
CREATE TABLE IF NOT EXISTS theta (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, utimestamp BIGINT, eeg1 FLOAT, eeg2 FLOAT, eeg3 FLOAT, eeg4 FLOAT, aux1 FLOAT, aux2 FLOAT); -- IXNMuseDataPacketTypeThetaAbsolute
CREATE TABLE IF NOT EXISTS gamma (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, utimestamp BIGINT, eeg1 FLOAT, eeg2 FLOAT, eeg3 FLOAT, eeg4 FLOAT, aux1 FLOAT, aux2 FLOAT); -- IXNMuseDataPacketTypeGammaAbsolute
CREATE TABLE IF NOT EXISTS good (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, utimestamp BIGINT, eeg1 FLOAT, eeg2 FLOAT, eeg3 FLOAT, eeg4 FLOAT, aux1 FLOAT, aux2 FLOAT); -- IXNMuseDataPacketTypeIsGood
CREATE TABLE IF NOT EXISTS hsi (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, utimestamp BIGINT, eeg1 FLOAT, eeg2 FLOAT, eeg3 FLOAT, eeg4 FLOAT, aux1 FLOAT, aux2 FLOAT); -- IXNMuseDataPacketTypeHsiPrecision 

-- http://ios.choosemuse.com/_i_x_n_accelerometer_8h.html
CREATE TABLE IF NOT EXISTS accelerometer (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, utimestamp BIGINT, x FLOAT, y FLOAT, z FLOAT, fb FLOAT, ud FLOAT, lr FLOAT); -- IXNMuseDataPacketTypeAccelerometer
-- http://ios.choosemuse.com/_i_x_n_gyro_8h.html
CREATE TABLE IF NOT EXISTS gyro (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, utimestamp BIGINT, x FLOAT, y FLOAT, z FLOAT, fb FLOAT, ud FLOAT, lr FLOAT); -- IXNMuseDataPacketTypeGyro

-- http://ios.choosemuse.com/_i_x_n_muse_artifact_packet_8h_source.html
CREATE TABLE IF NOT EXISTS artifact (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, utimestamp BIGINT, headband BOOLEAN, blink BOOLEAN, jaw BOOLEAN); -- IXNMuseDataPacketTypeArtifacts

-- https://developer.apple.com/documentation/corelocation/cllocation
CREATE TABLE IF NOT EXISTS location (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, utimestamp BIGINT, latitude FLOAT, longitude FLOAT, altitude FLOAT); -- CLLocation

-- https://developer.apple.com/documentation/coremotion/cmdevicemotion/1616149-useracceleration
CREATE TABLE IF NOT EXISTS acceleration (id BIGINT PRIMARY KEY AUTO_INCREMENT, subject_id INT, timestamp TIMESTAMP, utimestamp BIGINT, x FLOAT, y FLOAT, z FLOAT, fb FLOAT, ud FLOAT, lr FLOAT); -- CMAcceleration
