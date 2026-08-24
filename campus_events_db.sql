-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 24, 2026 at 05:00 PM
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
-- Database: `campus_events_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `club`
--

CREATE TABLE `club` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `club`
--

INSERT INTO `club` (`id`, `name`, `description`) VALUES
(1, 'Hell Fire', 'for gaming'),
(2, 'jk', 'for code base'),
(3, 'Star', 'for exam related'),
(4, 'jkadas', 'for code base'),
(5, 'Open Student', 'For Discussion'),
(6, 'LJ Institute Of Engineering & Technology', 'Collage Official Club');

-- --------------------------------------------------------

--
-- Table structure for table `event`
--

CREATE TABLE `event` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `event_date` date DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `club_id` int(11) DEFAULT NULL,
  `form_link` varchar(255) DEFAULT NULL,
  `poster` varchar(255) DEFAULT NULL,
  `reg_start` date DEFAULT NULL,
  `reg_end` date DEFAULT NULL,
  `capacity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `event`
--

INSERT INTO `event` (`id`, `title`, `event_date`, `location`, `description`, `club_id`, `form_link`, `poster`, `reg_start`, `reg_end`, `capacity`) VALUES
(1, 'CRAVOITIC 2.0', '2026-03-10', 'lj campus', 'Tech and innovation event.', 6, 'https://forms.gle/koG3BUcTgygv8sAUA', 'event1.jpeg', '2026-02-18', '2026-03-07', 150),
(2, 'CANVAS COUTURE', '2026-03-05', 'Ground', 'Art and fashion event.', 5, 'https://forms.gle/koG3BUcTgygv8sAUA', 'event2.jpeg', '2026-02-18', '2026-02-28', 200),
(3, 'DROBOTICS', '2026-03-01', 'lj campus', 'Robotics showcase and competition.', 2, 'https://forms.gle/koG3BUcTgygv8sAUA', 'event3.jpeg', '2026-02-18', '2026-02-25', 100),
(4, 'Checkmate Champion International Rapid Rating Tournament - 2026', '2026-03-15', 'Ground', 'Chess tournament.', 6, 'https://forms.gle/koG3BUcTgygv8sAUA', 'event4.jpeg', '2026-02-18', '2026-03-12', 300);

-- --------------------------------------------------------

--
-- Table structure for table `news`
--

CREATE TABLE `news` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `poster` varchar(255) DEFAULT NULL,
  `date_posted` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `news`
--

INSERT INTO `news` (`id`, `title`, `description`, `poster`, `date_posted`) VALUES
(1, 'LJ University Launches Innovation Hub', 'LJ University has inaugurated a state-of-the-art Innovation Hub, designed to foster creativity, research, and entrepreneurship among students. The hub will serve as a collaborative space for startups, industry partnerships, and academic projects.', 'n1.jpeg', '2026-02-20 10:00:00'),
(2, 'Annual Cultural Fest Brings Campus Alive', 'The vibrant annual cultural festival at LJ University showcased student talent in music, dance, theater, and art. With participation from across departments, the event highlighted the university’s commitment to holistic education and cultural diversity.', 'n2.jpeg', '2026-02-21 11:30:00'),
(3, 'LJ University Ranked Among Top Institutions', 'In a recent survey, LJ University secured a place among the top educational institutions in Gujarat, recognized for its academic excellence, modern infrastructure, and strong industry connections.', 'n3.jpeg', '2026-02-22 09:15:00'),
(4, 'Green Campus Initiative Gains Momentum', 'LJ University has expanded its sustainability efforts with a new Green Campus Initiative. From solar energy installations to eco-friendly practices, the university is setting an example in environmental responsibility.', 'n4.jpeg', '2026-02-23 14:45:00'),
(5, 'Students Shine in National Tech Competition', 'A team of LJ University students won accolades at a national-level technology competition, impressing judges with their innovative solutions in AI and robotics. Their achievement reflects the university’s focus on practical learning and cutting-edge research.', 'n5.jpeg', '2026-02-24 16:20:00');

-- --------------------------------------------------------

--
-- Table structure for table `participation`
--

CREATE TABLE `participation` (
  `user_id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `participation`
--

INSERT INTO `participation` (`user_id`, `event_id`) VALUES
(2, 1),
(2, 3),
(3, 2),
(4, 1),
(4, 4);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_admin` tinyint(1) DEFAULT 0,
  `club_id` int(11) DEFAULT NULL,
  `profile_picture` varchar(255) DEFAULT 'default_avatar.png'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `name`, `email`, `password`, `is_admin`, `club_id`, `profile_picture`) VALUES
(1, 'Admin', 'admin@gmail.com', 'admin123', 1, 6, 'default_avatar.png'),
(2, 'John Doe', 'john.doe@example.com', 'hashed_password_456', 0, 1, 'logo.png'),
(3, 'Jane Smith', 'jane.smith@example.com', 'hashed_password_789', 0, 2, 'default_avatar.png'),
(4, 'Alex Johnson', 'alex.j@example.com', 'hashed_password_012', 0, 3, 'default_avatar.png');

-- --------------------------------------------------------

--
-- Table structure for table `user_club`
--

CREATE TABLE `user_club` (
  `user_id` int(11) DEFAULT NULL,
  `club_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_club`
--

INSERT INTO `user_club` (`user_id`, `club_id`) VALUES
(2, 2);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `club`
--
ALTER TABLE `club`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `event`
--
ALTER TABLE `event`
  ADD PRIMARY KEY (`id`),
  ADD KEY `club_id` (`club_id`);

--
-- Indexes for table `news`
--
ALTER TABLE `news`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `participation`
--
ALTER TABLE `participation`
  ADD PRIMARY KEY (`user_id`,`event_id`),
  ADD KEY `event_id` (`event_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `club_id` (`club_id`);

--
-- Indexes for table `user_club`
--
ALTER TABLE `user_club`
  ADD KEY `user_id` (`user_id`),
  ADD KEY `club_id` (`club_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `club`
--
ALTER TABLE `club`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `event`
--
ALTER TABLE `event`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `news`
--
ALTER TABLE `news`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `event`
--
ALTER TABLE `event`
  ADD CONSTRAINT `event_ibfk_1` FOREIGN KEY (`club_id`) REFERENCES `club` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `participation`
--
ALTER TABLE `participation`
  ADD CONSTRAINT `participation_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `participation_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `event` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_ibfk_1` FOREIGN KEY (`club_id`) REFERENCES `club` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `user_club`
--
ALTER TABLE `user_club`
  ADD CONSTRAINT `user_club_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  ADD CONSTRAINT `user_club_ibfk_2` FOREIGN KEY (`club_id`) REFERENCES `club` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
