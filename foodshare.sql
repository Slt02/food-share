-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Εξυπηρετητής: 127.0.0.1:3306
-- Χρόνος δημιουργίας: 29 Μάη 2025 στις 22:19:37
-- Έκδοση διακομιστή: 10.4.32-MariaDB
-- Έκδοση PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Βάση δεδομένων: `foodshare`
--

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `donations`
--

CREATE TABLE `donations` (
  `id` int(11) NOT NULL,
  `donor_id` int(11) NOT NULL,
  `item_name` varchar(100) NOT NULL,
  `quantity` int(11) NOT NULL,
  `donation_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `donations`
--

INSERT INTO `donations` (`id`, `donor_id`, `item_name`, `quantity`, `donation_date`) VALUES
(1, 4, 'Fresh Vakalaos', 10, '2025-05-29 23:17:29');

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `food_requests`
--

CREATE TABLE `food_requests` (
  `id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `delivery_address` varchar(255) DEFAULT NULL,
  `number_of_people` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `delivery_status` varchar(50) DEFAULT 'Not Delivered/Pending',
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `food_requests`
--

INSERT INTO `food_requests` (`id`, `customer_id`, `delivery_address`, `number_of_people`, `status`, `delivery_status`, `created_at`) VALUES
(1, 3, 'Triwn Navarxwn 23', 3, 'pending', 'Not Delivered/Pending', '2025-05-29 23:11:13'),
(2, 3, 'Kanakari 160', 5, 'delivered', 'Delivered', '2025-05-29 23:13:27');

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `food_request_items`
--

CREATE TABLE `food_request_items` (
  `request_id` int(11) DEFAULT NULL,
  `item_name` varchar(100) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `food_request_items`
--

INSERT INTO `food_request_items` (`request_id`, `item_name`, `quantity`) VALUES
(1, 'Chicken Teriyaki', 1),
(1, 'Panakota', 1),
(2, 'Chicken Teriyaki', 3);

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `inventory`
--

CREATE TABLE `inventory` (
  `item_id` int(11) NOT NULL,
  `item_name` varchar(40) NOT NULL,
  `description` text DEFAULT NULL,
  `category` varchar(20) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `inventory`
--

INSERT INTO `inventory` (`item_id`, `item_name`, `description`, `category`, `quantity`) VALUES
(1, 'Chicken Teriyaki', 'Marinated with sesame and honey sauce!', 'Meat', 6),
(2, 'Fasolada', 'Amazing Homemade Greek Food', 'vegetables', 10),
(3, 'Panakota', 'Creamy Italian dessert made by simmering sweetened cream and thickening it with gelatin. It\'s smooth, delicate, and often served with fruit, caramel, or chocolate sauce for a delicious finish.', 'sweet', 9);

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `reports`
--

CREATE TABLE `reports` (
  `report_id` int(11) NOT NULL,
  `request_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `description` text NOT NULL,
  `reported_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `reports`
--

INSERT INTO `reports` (`report_id`, `request_id`, `customer_id`, `description`, `reported_at`) VALUES
(1, 2, 3, 'The chicken was almost raw! Please do something about it!', '2025-05-29 20:15:25');

-- --------------------------------------------------------

--
-- Δομή πίνακα για τον πίνακα `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `surname` varchar(50) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `role` enum('admin','customer','donor','dropoffagent') NOT NULL DEFAULT 'customer'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Άδειασμα δεδομένων του πίνακα `users`
--

INSERT INTO `users` (`id`, `name`, `surname`, `username`, `email`, `phone`, `password`, `created_at`, `role`) VALUES
(1, 'George', 'Clooney', 'admin', 'admin@example.com', '1234567890', 'admin', '2025-05-29 19:55:05', 'admin'),
(2, 'Kwstas', 'Papadopoulos', 'kwst_pap', 'dropoff@example.com', '1231231230', 'dropoff1', '2025-05-29 19:56:39', 'dropoffagent'),
(3, 'Dimitris', 'Kwstenoglou', 'customer', 'customer@example.com', '7894562130', 'Customer1!', '2025-05-29 19:57:27', 'customer'),
(4, 'Anastasis', 'Barlos', 'donor', 'donor@example.com', '1472583690', 'Donor123!', '2025-05-29 19:58:18', 'donor');

--
-- Ευρετήρια για άχρηστους πίνακες
--

--
-- Ευρετήρια για πίνακα `donations`
--
ALTER TABLE `donations`
  ADD PRIMARY KEY (`id`),
  ADD KEY `donor_id` (`donor_id`);

--
-- Ευρετήρια για πίνακα `food_requests`
--
ALTER TABLE `food_requests`
  ADD PRIMARY KEY (`id`);

--
-- Ευρετήρια για πίνακα `food_request_items`
--
ALTER TABLE `food_request_items`
  ADD KEY `request_id` (`request_id`);

--
-- Ευρετήρια για πίνακα `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`item_id`);

--
-- Ευρετήρια για πίνακα `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`report_id`),
  ADD KEY `request_id` (`request_id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- Ευρετήρια για πίνακα `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT για άχρηστους πίνακες
--

--
-- AUTO_INCREMENT για πίνακα `donations`
--
ALTER TABLE `donations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT για πίνακα `food_requests`
--
ALTER TABLE `food_requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT για πίνακα `inventory`
--
ALTER TABLE `inventory`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT για πίνακα `reports`
--
ALTER TABLE `reports`
  MODIFY `report_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT για πίνακα `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Περιορισμοί για άχρηστους πίνακες
--

--
-- Περιορισμοί για πίνακα `donations`
--
ALTER TABLE `donations`
  ADD CONSTRAINT `donations_ibfk_1` FOREIGN KEY (`donor_id`) REFERENCES `users` (`id`);

--
-- Περιορισμοί για πίνακα `food_request_items`
--
ALTER TABLE `food_request_items`
  ADD CONSTRAINT `food_request_items_ibfk_1` FOREIGN KEY (`request_id`) REFERENCES `food_requests` (`id`);

--
-- Περιορισμοί για πίνακα `reports`
--
ALTER TABLE `reports`
  ADD CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`request_id`) REFERENCES `food_requests` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `reports_ibfk_2` FOREIGN KEY (`customer_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
