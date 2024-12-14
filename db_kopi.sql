-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 13, 2024 at 06:38 AM
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
-- Database: `db_kopi`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `ID_Admin` int(10) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(70) NOT NULL,
  `alamat` varchar(50) NOT NULL,
  `email` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`ID_Admin`, `username`, `password`, `alamat`, `email`) VALUES
(4, 'haqiqi', '$2b$12$xpdg/82vRLC/QBO64EANH.KF5Nla5QEgr.O44kKFB8P.CxMdGEVxi', 'sudimoro', 'haqiqi@gmail.com'),
(5, 'admin', '$2b$12$sKT0Fg2MBoocmE9lhWwxCO.8jsk/rhYG5YUmiU9X3bdG5xQlO5KHK', 'adminku', 'adminku@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `message` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `contact`
--

INSERT INTO `contact` (`id`, `name`, `phone`, `email`, `message`) VALUES
(1, 'lu asik', '62895363206171', 'archfiendmnh@gmail.com', 'test test'),
(2, 'lu asik', '62895363206171', 'archfiendmnh@gmail.com', 'test test'),
(3, 'bang tapi bang', '62895363206171', 'archfiendmnh@gmail.com', 'test test');

-- --------------------------------------------------------

--
-- Table structure for table `keranjang`
--

CREATE TABLE `keranjang` (
  `id` int(11) NOT NULL,
  `url_gambar` varchar(255) NOT NULL,
  `nama_kopi` varchar(100) NOT NULL,
  `jumlah` int(11) NOT NULL,
  `harga` decimal(10,2) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `keranjang`
--

INSERT INTO `keranjang` (`id`, `url_gambar`, `nama_kopi`, `jumlah`, `harga`, `user_id`) VALUES
(25, '/static/files/images/black_coffee.png', 'Black Coffee', 1, 15000.00, 9),
(26, '/static/files/images/capuccino.jpeg', 'Cappuccino', 1, 20000.00, 9);

-- --------------------------------------------------------

--
-- Table structure for table `komplain`
--

CREATE TABLE `komplain` (
  `id` varchar(20) NOT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `jenis_keluhan` varchar(100) DEFAULT NULL,
  `isi_keluhan` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `komplain`
--

INSERT INTO `komplain` (`id`, `nama`, `jenis_keluhan`, `isi_keluhan`) VALUES
('#574826', 'haqiqi', 'error_transaksi', 'transaksi masih pending'),
('#672110', 'kenapa ya', 'error_website', 'error'),
('#686714', 'jorel', 'error_website', 'webiste 500 error kenapa ini?'),
('#752511', 'jorel', 'error_akun', 'akun saya bermaslah tidak bisa login'),
('#838797', 'jorel', 'error_akun', 'akun saya bermaslah tidak bisa login'),
('#842331', 'haqiqi', 'error_akun', 'akun saya dihack tolong solusi??'),
('#875202', 'api terbang', 'error_transaksi', 'transaksi saya tidak diproses padahal sudah membayar');

-- --------------------------------------------------------

--
-- Table structure for table `menu_kopi`
--

CREATE TABLE `menu_kopi` (
  `id` int(11) NOT NULL,
  `nama_kopi` varchar(255) NOT NULL,
  `gambar_url` varchar(255) NOT NULL,
  `harga` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu_kopi`
--

INSERT INTO `menu_kopi` (`id`, `nama_kopi`, `gambar_url`, `harga`) VALUES
(1, 'Black Coffee', '/static/files/images/black_coffee.png', 15000),
(2, 'Americano', '/static/files/images/iced_toddy.jpg', 20000),
(3, 'Cappuccino', '/static/files/images/capuccino.jpeg', 20000),
(4, 'Iced Latte', '/static/files/images/icedlatte.jpg', 22000),
(5, 'Macchiato', '/static/files/images/Caramel+Macchiato.jpg', 20000),
(6, 'Espresso', '/static/files/images/Shot-of-espresso.png', 15000);

-- --------------------------------------------------------

--
-- Table structure for table `transaksi`
--

CREATE TABLE `transaksi` (
  `id` int(11) NOT NULL,
  `transaction_no` varchar(50) NOT NULL,
  `nama_pelanggan` varchar(255) DEFAULT NULL,
  `metode_pembayaran` varchar(50) DEFAULT NULL,
  `waktu_transaksi` datetime DEFAULT NULL,
  `total_harga` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `ID_User` int(10) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(70) NOT NULL,
  `alamat` varchar(50) NOT NULL,
  `email` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`ID_User`, `username`, `password`, `alamat`, `email`) VALUES
(7, 'test', '$2b$12$z0ZUKoMJbMmux2fpzmX.EOsTB6YmJwpG0UX1Rr/SovE6IVKfUfaIi', 'sleman', 'tes@gmail.com'),
(8, 'anjay', '$2b$12$Y41O7rT2vGF51tod7rRCX.XE8tJLaxPTkhrsNVlGhVBahWiMU3sHG', 'anjay', 'anjay@gmail.com'),
(9, 'haqiqi', '$2b$12$/0mB3eIvR1db9I.lK9PYp.9ukWOnNz/YkndArz2FObViASF9npTta', 'haqiqi', 'hakiki2917@gmail.com'),
(10, 'aldo', '$2b$12$wbIcpEtIOp706u5b.V2QnOR4BKPkpQoW.p0HgaR7AmdhTGqwzhzSq', 'aldo', 'aldo@gmail.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`ID_Admin`);

--
-- Indexes for table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `keranjang`
--
ALTER TABLE `keranjang`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user` (`user_id`);

--
-- Indexes for table `komplain`
--
ALTER TABLE `komplain`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `menu_kopi`
--
ALTER TABLE `menu_kopi`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `transaksi`
--
ALTER TABLE `transaksi`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`ID_User`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `ID_Admin` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `contact`
--
ALTER TABLE `contact`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `keranjang`
--
ALTER TABLE `keranjang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `menu_kopi`
--
ALTER TABLE `menu_kopi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `transaksi`
--
ALTER TABLE `transaksi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `ID_User` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `keranjang`
--
ALTER TABLE `keranjang`
  ADD CONSTRAINT `fk_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`ID_User`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
