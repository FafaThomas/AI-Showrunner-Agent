INSERT INTO SLOT (
    start_time,
    end_time,
    duration_minutes,
    slot_name,
    daypart,
    is_prime_time
)
VALUES
('06:00', '07:00', 60, 'Early Morning', 'Morning', FALSE),
('07:00', '08:00', 60, 'Morning Drive', 'Morning', FALSE),
('18:00', '19:00', 60, 'Early Prime', 'Prime Time', TRUE),
('19:00', '20:00', 60, 'Prime 1', 'Prime Time', TRUE),
('20:00', '21:00', 60, 'Prime 2', 'Prime Time', TRUE),
('21:00', '22:00', 60, 'Late Prime', 'Prime Time', TRUE),
('22:00', '23:00', 60, 'Late Night', 'Late Night', FALSE);