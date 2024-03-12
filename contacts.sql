-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 19, 2024 at 11:06 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mybulletin`
--

-- --------------------------------------------------------

--
-- Table structure for table `contacts`
--

CREATE TABLE `contacts` (
  `serial` int(250) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(50) NOT NULL,
  `msg` text NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contacts`
--

INSERT INTO `contacts` (`serial`, `name`, `email`, `msg`, `date`) VALUES
(1, 'example', 'example@gmail.com', 'example', '2024-02-13 20:33:09'),
(3, 'Boudhik Chawda', 'boudhik.chawda72@gmail.com', 'Amazing website bro. Keep it up!!', '2024-02-13 22:53:33'),
(15, 'ssssss', 'jjihisdh@gmail.com', 'mmmmmmm', '2024-02-14 16:49:59'),
(16, 'ssssss', 'jjihisdh@gmail.com', 'mmmmmmm', '2024-02-14 16:52:52'),
(17, 'ssssss', 'jjihisdh@gmail.com', 'mmmmmmm', '2024-02-14 16:56:07'),
(18, 'ssssss', 'jjihisdh@gmail.com', 'mmmmmmm', '2024-02-14 16:56:51'),
(19, 'ssssss', 'jjihisdh@gmail.com', 'mmmmmmm', '2024-02-14 16:59:42'),
(20, 'ssssss', 'jjihisdh@gmail.com', 'mmmmmmm', '2024-02-14 17:01:43'),
(22, 'Boudhik Chawda', 'mastermind.7290@gmail.com', 'Daym bitch getting smart huh, Nice work Bro ', '2024-02-14 17:12:29'),
(23, 'kirit chawda', 'kiritchawda70@gmail.com', 'i like your activity, go ahead', '2024-02-14 18:29:09');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `contacts`
--
ALTER TABLE `contacts`
  ADD PRIMARY KEY (`serial`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contacts`
--
ALTER TABLE `contacts`
  MODIFY `serial` int(250) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=24;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
