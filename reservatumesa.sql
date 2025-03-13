-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: reservatumesa
-- ------------------------------------------------------
-- Server version	5.5.5-10.4.32-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client` (
  `client_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(15) NOT NULL,
  PRIMARY KEY (`client_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
INSERT INTO `client` VALUES (1,'ComeYCorre','$2b$12$ePD9tpUDBHwSyvIYWCQy3udrboj.LG7xXwZIVFud1NLA73HKQSd.S','678 123 456'),(2,'MesaQueMasAplauda','$2b$12$cfd25rxgyGyJFiVfOYR9ee9f/ANxtpe2HS0EKupFE5DKv4QY8H1qG','612 987 654'),(3,'Tragoncio22','$2b$12$Iv0VPmTI2lGewW/YUxlT8OPRO20Lm/wsFxiF.iGPteMbJYiO/QK5a','645 321 789'),(4,'SillaCaliente','$2b$12$VGCXFv8PmSJWadDnIR81hOREA/So3u/AdgkGVjEzVFDE2GB/0F0x6','690 456 123'),(5,'ComeTierraPro','$2b$12$w3z/6nGOMxF2mjgmZjj.cOnmOz/PTvge6Q.ZyO0F2rmYizfr8SnN.','655 789 321'),(6,'DameTuMesa','$2b$12$D88GNU69HPetABKkSeT0BeoGu3roIHLCpk4JoRzTgx77755oP6vee','687 234 567'),(7,'FullPlato99','$2b$12$sZSVjnOrxvRCKY8v.b10JOiwmAV5zMwNdLs76JrdTX4PMwsynql.m','620 345 678'),(8,'BarrigaLlenaVIP','$2b$12$1jwfzJij6GxqrEeKe9g23e73CAMX0zy/4lUxdldOjLIdYRNBKnC/e','699 876 543'),(9,'ReservoYNoVoy','$2b$12$2jJRG6H8Oc2MP4smnGW49eqpOZttQWgOG3zbOHAcoczETczkZj/Sq','635 210 987'),(10,'ReyDelTenedor','$2b$12$PgSOdL6vEfODcmTXUQ3aAOK9e01ErRxRl58Uys.i5Pgpx09DOEQ4W','670 432 156');
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reservation`
--

DROP TABLE IF EXISTS `reservation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reservation` (
  `reservation_id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) NOT NULL,
  `restaurant_id` int(11) NOT NULL,
  `diners` int(11) NOT NULL,
  `date` date NOT NULL,
  `time` time NOT NULL,
  `status` enum('pendiente','confirmada','cancelada') NOT NULL,
  PRIMARY KEY (`reservation_id`),
  KEY `client_id` (`client_id`),
  KEY `restaurant_id` (`restaurant_id`),
  CONSTRAINT `reservation_ibfk_1` FOREIGN KEY (`client_id`) REFERENCES `client` (`client_id`),
  CONSTRAINT `reservation_ibfk_2` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurant` (`restaurant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reservation`
--

LOCK TABLES `reservation` WRITE;
/*!40000 ALTER TABLE `reservation` DISABLE KEYS */;
/*!40000 ALTER TABLE `reservation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurant`
--

DROP TABLE IF EXISTS `restaurant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restaurant` (
  `restaurant_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `restaurant_name` varchar(100) NOT NULL,
  `capacity` int(11) NOT NULL,
  `website` varchar(255) DEFAULT NULL,
  `address` varchar(255) NOT NULL,
  `description` text DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`restaurant_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurant`
--

LOCK TABLES `restaurant` WRITE;
/*!40000 ALTER TABLE `restaurant` DISABLE KEYS */;
INSERT INTO `restaurant` VALUES (1,'ElReyDelBuffet ','$2b$12$GayWUl0kaswQoKBKla8xtO4vU1S4DfJyll1BAi/HZFkq/hE.lEVyC','678 901 234','El Rey del Buffet',40,'www.reydelbuffet.com','Calle del Atracón, 12','Buffet libre con más de 100 platos, postres ilimitados y bebidas incluidas.','elreydelbuffet.jpg'),(2,'TacoLcoco ','$2b$12$etyFl4lBbHztCrApxTQfsOLilAZ1CXiJUpX.NAcJ4nHer4Lal6lae','612 345 678','Taco Locco',30,'www.tacolocco.com','Avenida Picante, 45','Auténtica comida mexicana, tacos al pastor y nachos con queso fundido.','tacoloco.jpg'),(3,'FritangaVIP','$2b$12$bbdvUtEK4nbZemOGQeANwu8kB6xdJ31YkHmh6RHEAgHU.d.wv7dyi','645 789 123','Fritanga VIP',25,'www.fritangavip.com','Plaza del Aceite, 7','Especialidad en frituras de todo tipo, desde calamares hasta churros rellenos.','fritangavip.jpg'),(4,'Pizzarollit0','$2b$12$QkjT3JbNn9BgKQpZHWoFkORaW.HGdQLEWx0zh8sR1BsYLjC7s1yhq','690 234 567','Pizzarollito',35,'www.pizzarollito.com','Calle de la Masa, 99','Pizzería artesanal con horno de leña y opciones veganas.','pizzarolito.jpg'),(5,'HamburQueen','$2b$12$ueTa8wwQ6/oOsfmcGUjI4uE35xQeb/flqad69wqWK2wJomZaddb8e','655 876 432','HamburQueen',40,'www.hamburqueen.com','Paseo del Sabor, 21','Hamburguesas gourmet con ingredientes premium y salsas caseras.','hamburqueen.jpg'),(6,'ComeQueTeVas','$2b$12$Rbu2StmZbyxJGWLN..SLEu0c58/fCVdrnaV2xAKcZzlLryHsizzuO',' 687 321 098','Come Que Te Vas',20,'www.comequetevas.com','Camino del Hambre, 5','Menús rápidos para los que tienen prisa, sin perder sabor.','comequetevas.jpg'),(7,'SushiMunchies','$2b$12$TM1vlnYIiYvPSOXeD9son.pOU.2dfWTnveltwDHv/7Ja4YlP/j8Be','620 654 321','Sushi Munchies',30,'www.sushimunchies.com','Calle de la Soja, 10','Sushi fusión con opciones innovadoras y sabores únicos.','sushimunchies.jpg'),(8,'GordiPasta','$2b$12$8zPWG7a30nQWGWgJeVuee.7qoRvkVSFOrMGAKKv11po0tsBs2gGpq','699 210 876','GordiPasta',25,'www.gordipasta.com','Avenida Italiana, 88','Pastas caseras con salsas abundantes y pan de ajo ilimitado.','gordipasta.jpg'),(9,'WokAndRoll','$2b$12$/MxUnez8Yyfhq3.zGrvqi.9K/jOKU.mIdxEdQVBVgcHT3P.tW33ly','635 543 210','Wok & Roll',30,'www.wokandroll.com','Calle del Dragón, 23','Cocina asiática al wok con ingredientes frescos y show en vivo.','wokandroll.jpg'),(10,'PollosLocos','$2b$12$gmJiiUwrP/H7VPwlN3l0qu/bnF4KMmcacHILGt2z07wLzpN9PK0Te','670 876 543','Pollos Locos',40,'www.polloslocos.com',' Plaza del Asador, 14','Especialistas en pollo frito crujiente y salsas caseras.','polloslocos.jpg'),(11,'CarnivoroXtreme','$2b$12$qa6mGPG0IdSOLiyh/V0UjuOZkoxb1FYGhn8rXUup1RF6qhmbjAG3K','658 987 432','Carnívoro Xtreme',35,'www.carnivoroxtreme.com','Calle de la Barbacoa, 66','Parrillada de carnes con cortes premium y chimichurri casero.','carnivoroxtreme.jpg'),(12,'EmpanadaPower','$2b$12$yLdH8ZpXnj/yiplsY8wyh.EAYFLmH1ghb5VCyU.lXbWndCbuSNNce','625 432 678','Empanada Power',20,'www.empanadapower.com','Calle del Horno, 3','Empanadas argentinas y venezolanas con variedad de rellenos.','empanadapower.jpg'),(13,'VeggieLover','$2b$12$G3bCdCMUWtCJVwHZ46G1luieZnJRKa.flX9LPHbetoSlUGxBoO.ji',' 681 210 654','Veggie Lover',25,'www.veggielover.com','Paseo Verde, 11','Cocina vegetariana con ingredientes frescos y orgánicos.','veggielover.jpg'),(14,'ChocoLoco','$2b$12$oUf90qNOxvg0zN/Evy1wSutwcDqX9VZr/6Tbbg8KW3m3v6CFsiqGS','689 567 890','ChocoLoco',15,'www.chocoloco.com',' Calle del Cacao, 50','Postres y bebidas de chocolate en todas sus formas.','chocoloco.jpg'),(15,'PatataBrava','$2b$12$QZGnKwQ/7XOcNcoqyn6mhuAidYlti/FQU1Snex52TFx2xDj6Bb3Py','674 678 321','Patata Brava',20,'www.patatabrava.com','Avenida de las Tapas, 8','Especialidad en patatas bravas con salsas caseras.','patatabrava.jpg'),(16,'Marisquito','$2b$12$.ko315AkJ//Xqyijaa2pbObBmZxAYvGSgK409gsElRCC0zAk1FF0e','663 345 987','Marisquito',35,'www.marisquito.com','Paseo Marítimo, 17','Mariscos frescos y paellas con ingredientes de primera calidad.','marisquito.jpg'),(17,'ArepaFest','$2b$12$7TXLFLEAIhMzCa21qrMAyuBBTBeOdVwJL.bj/67PWIQI7cPV10WhK',' 611 789 234','Arepa Fest',25,'www.arepafest.com','Calle de la Harina, 22',' Arepas rellenas al mejor estilo venezolano y colombiano.','arepafest.jpg'),(18,'RolloPrimavera','$2b$12$ErHvLb2lJ2mV3v2aVO9hCOs1ZyMx5bWkJJX6nIVC7dwUOe.koOxZ2','648 654 789','Rollo Primavera',30,'www.rolloprimavera.com','Barrio Chino, 29','ocina asiática con especialidad en rollitos de primavera y dumplings.','rolloprimavera.jpg'),(19,'TodoAlHorno','$2b$12$hsiO8pmRbzd/G7e6NR0PYOzk7HK7lkwc5eIsiaMylBVfPdLdN215S','630 876 210','Todo al Horno',40,' www.todoalhorno.com','Calle del Fuego, 77','Platos cocinados al horno para una experiencia sin frituras.','todoalhorno.jpg'),(20,'CucharaDeOro','$2b$12$OjezuacEZf0Vk0xrV/V9DeDryFZogkHfmtq17QjqJPUkYkRJzkqKC','679 543 876','Cuchara de Oro',25,'www.cucharadeoro.com','Calle de la Abuela, 6','Comida casera con recetas tradicionales y sopas abundantes.','cucharadeoro.jpg');
/*!40000 ALTER TABLE `restaurant` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-13 14:31:22
