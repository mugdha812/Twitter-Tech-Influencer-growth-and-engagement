library(dplyr)
library(readr)
library(ggplot2)


tweets <- read_csv("C:/Users/shlok/OneDrive/Documents/data visualization/New folder/tweets.csv")
users <- read_csv("C:/Users/shlok/OneDrive/Documents/data visualization/New folder/users.csv")
profile_snapshots <-read_csv("C:/Users/shlok/OneDrive/Documents/data visualization/New folder/profile_snapshots.csv")
likes <- read_csv("C:/Users/shlok/OneDrive/Documents/data visualization/New folder/likes.csv")


likes_count <- likes %>%
  group_by(tweetId) %>%
  summarise(likes_count = n())


tweets <- left_join(tweets, likes_count, by = "tweetId")


tweets$likes_count[is.na(tweets$likes_count)] <- 0


tweets <- tweets %>%
  mutate(engagement = favorite_count + retweet_count + likes_count)


user_engagement <- tweets %>%
  group_by(twitterUserId) %>%
  summarise(total_engagement = sum(engagement, na.rm = TRUE),
            tweet_count = n())


latest_followers <- profile_snapshots %>%
  group_by(twitterUserId) %>%
  summarise(followers_count = last(followers_count))


user_data <- user_engagement %>%
  left_join(latest_followers, by = "twitterUserId") %>%
  left_join(users %>% select(twitterUserId, display_name), by = "twitterUserId")


user_data <- user_data %>%
  mutate(InformationSpreadability = followers_count + tweet_count * total_engagement)


top_users <- user_data %>%
  arrange(desc(InformationSpreadability)) %>%
  slice_max(order_by = InformationSpreadability, n = 10)


ggplot(top_users, aes(x = reorder(display_name, InformationSpreadability), y = InformationSpreadability)) +
  geom_col(fill='blue') +
  coord_flip() +
  labs(title = "Top Influencers by Information Spreadability",
       x = "Display Name",
       y = "Information Spreadability")
