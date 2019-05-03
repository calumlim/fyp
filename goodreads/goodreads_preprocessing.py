#goodreads data preprocessing

import pandas as pd
import math
import time
import numpy
import csv

df = pd.read_csv('br_gk.csv', header=0)
column_bookID = df['bookID']
column_title = df['title']
column_author = df['author']
column_avg_rating = df['rating']
column_ratings_count = df['ratingsCount']
column_reviews_count = df['reviewsCount']
column_reviewer_name = df['reviewerName']
column_user_rating = df['reviewerRatings']
column_text_review = df['review']

def mean_rating(arr):
    n = len(arr)
    mean_val = 0
    count = 0
    for i in range(n):
        if math.isnan(arr[i])!=True:
            mean_val+=float(arr[i])
            count+=1
    mean_val = mean_val/count
    return mean_val

def review_avg_text_count(arr):
    n = len(arr)
    avg_len = 0
    count = 0
    for i in range(n):
        if type(arr[i])!=float:
            avg_len+=len(arr[i].split(" "))
            count+=1
    avg_len = avg_len/count
    return avg_len
def count_unique_users():
    f = open("unique_users.txt", "w")
    n = len(column_reviewer_name)
    unique_users_arr = []
    count = 0
    user_arr = return_array(column_reviewer_name)
    for i in range(n):
        current_user = str(user_arr[i])
        if current_user!='None':
            if i%250==0:
                print("Current progress: ", i, current_user)
            f.write(str(current_user)+"\n")
            for j in range(0,n):
                #unique_users_arr.append(current_user)
                count+=1
                next_user = str(user_arr[j])
                if current_user==next_user:
                    user_arr[j] = None
    f.write(str(count))
    f.close()
    return len(unique_users_arr)
def count_unique_books():
    # n = len(column_title)
    f = open('duplicate_books_data.txt', "w+")
    n = len(column_title)
    title_arr = return_array(column_title)
    review_arr = return_array(column_text_review)
    count_books = []
    duplicate_index = []

    for i in range(n):
        if i%250==0:
            print("Checking duplicate data...", i)
        duplicate_index_tmp = []
        current_book = str(title_arr[i])
        if current_book!='None':
            duplicate_index_tmp.append(current_book)
            start_time = time.time()
            count_duplicate = 0
            for j in range(0,n):
                next_book = str(title_arr[j])
                if next_book==current_book:
                    count_duplicate+=1
                    duplicate_index_tmp.append(j)
                    title_arr[j]=None
            count_books.append([current_book, count_duplicate])
            duplicate_index.append(duplicate_index_tmp)
            f.write(str(duplicate_index_tmp)+"\n")
            # print(duplicate_index_tmp)
        # print([current_book, count_duplicate], "Time taken: "+ str(time.time()-start_time), len(title_arr))
    f.close()
    return [count_books, duplicate_index]

def min_max(arr):
    min_val = int(arr[0])
    max_val = int(arr[0])

    for i in range(len(arr)):
        if int(arr[i])<min_val:
            min_val = int(arr[i])
        if int(arr[i])>max_val:
            max_val = int(arr[i])
    return [min_val, max_val]

def return_array(arr):
    new_arr = []
    for i in range(len(arr)):
        new_arr.append(arr[i])
    return new_arr

def print_duplicate_info(arr):
    # book_arr = return_array(column_bookID)
    # author_arr = return_array(column_author)
    # avg_rating_arr = return_array(column_avg_rating)
    # rating_count_arr = return_array(column_ratings_count)
    # review_count_arr = return_array(column_reviews_count)
    # reviewer_arr = return_array(column_reviewer_name)
    review_text_arr = return_array(column_text_review)

    for i in range(len(arr)):
        if len(arr[i])-1>1:
            print("Title: ", arr[i][0], "Count: ", len(arr[i])-1, arr[i])
            for j in range(1,len(arr[i])):
                if type(review_text_arr[arr[i][j]])==float:
                    print(review_text_arr[arr[i][j]])
                else:
                    if len(review_text_arr[arr[i][j]])>50:
                        print(review_text_arr[arr[i][j]][0:50])
            print("\n")
def data_cleanup():
    #delete rows without rating and review
    #delete duplicate book title rows
    #sort in alphabetical order

    book_arr = return_array(column_bookID)
    title_arr = return_array(column_title)
    author_arr = return_array(column_author)
    avg_rating_arr = return_array(column_avg_rating)
    rating_count_arr = return_array(column_ratings_count)
    review_count_arr = return_array(column_reviews_count)
    reviewer_arr = return_array(column_reviewer_name)
    reviewer_rating_arr = return_array(column_user_rating)
    review_text_arr = return_array(column_text_review)

    print("Reading data done!\n")

    print("Duplicate thots be gone!\n")
    #delete duplicate book title rows
    duplicate_index_arr = count_unique_books()[1]       #obtain the duplicate books info array
    offset = 0
    for i in range(len(duplicate_index_arr)):
        if i%250==0:
            print("Duplicate thots begone progress: ", i)
        if len(duplicate_index_arr[i])>2:
            for j in range(1,len(duplicate_index_arr[i])):
                if duplicate_index_arr[i][j]!=None:
                    current_review_text = review_text_arr[duplicate_index_arr[i][j]-offset]
                    for k in range(2, len(duplicate_index_arr[i])):
                        if k!=j:
                            if duplicate_index_arr[i][k]!=None:
                                compare_review_text = review_text_arr[duplicate_index_arr[i][k]-offset]

                                # if type(current_review_text)!=float and type(compare_review_text)!=float:
                                #     print([i,j])
                                #     print(current_review_text[0:50])
                                #     print(compare_review_text[0:50])
                                #     print()
                                if current_review_text==compare_review_text:
                                    book_arr.pop(duplicate_index_arr[i][k]-offset)
                                    title_arr.pop(duplicate_index_arr[i][k]-offset)
                                    author_arr.pop(duplicate_index_arr[i][k]-offset)
                                    avg_rating_arr.pop(duplicate_index_arr[i][k]-offset)
                                    rating_count_arr.pop(duplicate_index_arr[i][k]-offset)
                                    review_count_arr.pop(duplicate_index_arr[i][k]-offset)
                                    reviewer_arr.pop(duplicate_index_arr[i][k]-offset)
                                    reviewer_rating_arr.pop(duplicate_index_arr[i][k]-offset)
                                    review_text_arr.pop(duplicate_index_arr[i][k]-offset)

                                    # print("Destroyed row at index: ", duplicate_index_arr[i][k])
                                    duplicate_index_arr[i][k] = None
                                    offset+=1
                    #print("array: ", duplicate_index_arr[i])
    print("GTFO Duplicate data time!\n")
    #delete duplicate book title rows
    i = 0
    n = len(review_text_arr)
    offset = 0
    while i<n:
        if i%250==0:
            print("GTFO Duplicate rows progress: ", i)
        # print(i, type(review_text_arr[i]), type(reviewer_rating_arr[i]))
        if type(review_text_arr[i-offset])==float and isinstance(reviewer_rating_arr[i-offset], numpy.float64)==True:
            book_arr.pop(i-offset)
            title_arr.pop(i-offset)
            author_arr.pop(i-offset)
            avg_rating_arr.pop(i-offset)
            rating_count_arr.pop(i-offset)
            review_count_arr.pop(i-offset)
            reviewer_arr.pop(i-offset)
            reviewer_rating_arr.pop(i-offset)
            review_text_arr.pop(i-offset)

            # print(len(review_text_arr))
            offset+=1
            n-=1
        i+=1
    
    f = open("cleaned_dataset.txt", "w")
    for i in range(len(review_text_arr)):
        if i%250==0:
            print("Writing data....", i, "out of", len(review_text_arr))
        f.write(str(book_arr[i])+"\t"+str(title_arr[i])+"\t"+str(author_arr[i])+"\t"+str(avg_rating_arr[i])+"\t"+str(rating_count_arr[i])+"\t"+str(review_count_arr[i])+"\t"+str(reviewer_arr[i])+"\t"+str(reviewer_rating_arr[i])+"\t"+str(review_text_arr[i])+"\n")
    f.write(str(len(review_text_arr)))
    f.close()

def sort_cleaned_data_by_title():
    f = open('cleaned_dataset.txt', 'r+')
    g = open('cleaned_dataset_sorted_title.txt', 'w+')
    final_arr = []
    for i in range(28):
        final_arr.append([])

    for line in f:
        line_split = line.split('\t')
        if len(line_split)>2:
            if len(line_split[1][0].lower())>1:
                final_arr[27].append(line)
                # print("Others:\t", line_split[1][0])
            elif ord(line_split[1][0].lower())-97<0 or ord(line_split[1][0].lower())-97>27:
                final_arr[27].append(line)
                # print("Others:\t", line_split[1][0], ord(line_split[1][0].lower())-97)
            else:
                final_arr[ord(line_split[1][0].lower())-97].append(line)
                # print("Else:\t", line_split[1][0], ord(line_split[1][0].lower())-97)
    for i in range(len(final_arr)):
        print(i)
        if i!=len(final_arr):
            for j in range(len(final_arr[i])):
                for k in range(0, len(final_arr[i])-j-1): 
                    if len(final_arr[i][k].split('\t')[1]) > len(final_arr[i][k+1].split('\t')[1]):
                        final_arr[i][k], final_arr[i][k+1] = final_arr[i][k+1], final_arr[i][k]
                # print(final_arr[i][j].split('\t')[1])
        else:
            for j in range(len(final_arr[i])):
                for k in range(0, len(final_arr[i])-j-1): 
                    if len(final_arr[i][k].split('\t')[1]) > len(final_arr[i][k+1].split('\t')[1]):
                        final_arr[i][k], final_arr[i][k+1] = final_arr[i][k+1], final_arr[i][k]
                # print(final_arr[i][j].split('\t')[1])
    
    for i in range(len(final_arr)):
        if i!=len(final_arr):
            for j in range(len(final_arr[i])):
                g.write(final_arr[i][j])
                # print(final_arr[i][j].split('\t')[1])
        else:
            for j in range(len(final_arr[i])):
                g.write(final_arr[i][j])
                # print(final_arr[i][j].split('\t')[1])
    
    g.close()
    f.close()
def write_csv(header, filename):
    f = open(filename, "r+")

    with open(filename+".csv", mode='w') as csv_file:
        fieldnames = header
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        count = 0
        writer.writeheader()
        for line in f:
            if count%10==0:
                print("Progress: ", count)
            line_split = line.split('\t')
            line_split[-1] = line_split[-1].replace('\n', '')
            
            if len(line_split)>len(header):
                extra_column = ""
                for i in range(len(header), len(line_split)):
                    extra_column+=line_split[i]
                for i in range(len(header), len(line_split)+1):
                    line_split.pop()
                line_split.append(extra_column)
            row_data = {}
            for i in range(len(line_split)):
                row_data[header[i]] = line_split[i]
            writer.writerow(row_data)
            count+=1


    
# print(len(column_bookID))
# print(min_max(column_bookID))
# print_duplicate_info(count_unique_books()[1])
# print(count_unique_users())
# count_unique_books()
# print("Mean rating: ",mean_rating(column_user_rating))
# print("Avg. length of review: ",review_avg_text_count(column_text_review))
# data_cleanup()
# sort_cleaned_data_by_title()



csv_header = ["bookID", "title", "author", "avg_rating", "total_rating", "total_review", "reviewer_name", "reviewer_rating", "review"]
write_csv(csv_header, "cleaned_dataset_sorted_title.txt")