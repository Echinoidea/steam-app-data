# Read JSON file containing Steam App data
# Make histogram of app review percentage

library("rjson")

json_file <- fromJSON(file = "C:/_dev/PYTHON/DATA/SteamAppData/topsellers_all_5000_minreview50.json")

options(scipen = 50)
positives <- lapply(json_file, '[[', 6)
negatives <- lapply(json_file, '[[', 7)
df <- rbind(as.data.frame(positives), as.data.frame(negatives))
df[nrow(df) + 1,] = df[1,] + df[2,]
df[nrow(df) + 1,] = df[1,] / df[3,]
rownames(df) = c("POS", "NEG", "TOTAL", "PERC")
hist(t(df[4,]), ylim=c(0,1000), labels=TRUE, main="Positive Review Percentage Frequency for Top 5000 INDIE&PUBLISHER Steam Apps", breaks=seq(0.2, 1.0, 0.025))

json_file <- fromJSON(file = "C:/_dev/PYTHON/DATA/SteamAppData/topsellers_indie_5000_minreview50.json")

options(scipen = 50)
positives <- lapply(json_file, '[[', 6)
negatives <- lapply(json_file, '[[', 7)
df <- rbind(as.data.frame(positives), as.data.frame(negatives))
df[nrow(df) + 1,] = df[1,] + df[2,]
df[nrow(df) + 1,] = df[1,] / df[3,]
rownames(df) = c("POS", "NEG", "TOTAL", "PERC")
hist(t(df[4,]), ylim=c(0,1000), labels=TRUE, main="Positive Review Percentage Frequency for Top 5000 INDIE Steam Apps", breaks=seq(0.2, 1.0, 0.025))

json_file <- fromJSON(file = "C:/_dev/PYTHON/DATA/SteamAppData/topsellers_publisher_5000_minreview50.json")

options(scipen = 50)
positives <- lapply(json_file, '[[', 6)
negatives <- lapply(json_file, '[[', 7)
df <- rbind(as.data.frame(positives), as.data.frame(negatives))
df[nrow(df) + 1,] = df[1,] + df[2,]
df[nrow(df) + 1,] = df[1,] / df[3,]
rownames(df) = c("POS", "NEG", "TOTAL", "PERC")
hist(t(df[4,]), ylim=c(0,1000), labels=TRUE, main="Positive Review Percentage Frequency for Top 5000 PUBLISHER Steam Apps", breaks=seq(0.2, 1.0, 0.025))
