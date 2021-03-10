
library(dplyr)
library(tidyr)

df <- read.csv('D://shopee/contacts.csv', header = T, row.names = 1) 
df <- as.data.frame(df)

df$Email <- as.character(df$Email)
df$Email[df$Email==""]<-NA
df$OrderId <- as.character(df$OrderId)
df$OrderId[df$OrderId==""]<-NA
df$Contacts <- as.numeric(df$Contacts)
saveRDS(df,'contatcs.rds')


start_time <- Sys.time()
df <- readRDS('D://shopee/contatcs.rds')  
df$row <- row.names(df)    
#df <- df[which(df$Id %in% c(215197, 50, 404324, 5, 212533, 226720, 458692, 383605, 482810)),]
df <- df %>% group_by(Email) %>% mutate( row = ifelse(is.na(Email), Id, max(Id)))

time1 <- Sys.time()
# by phone
phone <- df %>% filter(!is.na(Phone)) %>% group_by(Phone) %>% summarise(n=n())
phone <- phone[which(phone$n>1),1]

for (i in c(1:nrow(phone))){
  # get the phone
  p = phone$Phone[i]
  # find the max 'row', to set the 'row'
  max <- max(df$row[which(df$Phone==p)])
  # find all current 'row' of the macthed phone
  toChangeRow = df$row[which(df$Phone==p)]
  df$row[which(df$row %in% toChangeRow)] <- max
}
time2 <- Sys.time()

#by orderId
order <- df %>% filter(!is.na(OrderId)) %>% group_by(OrderId) %>% summarise(n=n())
order <- order[which(order$n>1),1]

for (i in c(1:nrow(order))){
  o = order$OrderId[i]
  # find the max row, to set the 'row'
  max <- max(df$row[which(df$OrderId==o)])
  # find current row of the macthed phone
  toChangeRow = df$row[which(df$OrderId==o)]
  df$row[which(df$row %in% toChangeRow)] <- max
}
end_time <- Sys.time()
saveRDS(df,'result.rds')


# output
df <- df %>% group_by(row) %>% mutate( trace = paste(Id, collapse = '-'))
df <- df %>% group_by(row) %>% mutate( sum = sum(Contacts,na.rm = TRUE))
df <- df %>% mutate( `ticket_trace/contact` = paste(trace, sum, sep = ','))

output <- df[,c(1,9)]
colnames(output) <- c('ticket_id', 'ticket_trace/contact')
saveRDS(output,'output.rds')
write.csv(output,'output.csv',row.names = FALSE)





