# Importing the needed libraries, BeautifulSoup for scraping and requests for accessing websites.
from bs4 import BeautifulSoup
import requests

# Custom search option for the user.
print ( 'What is the keyword you wish to search with?' )
keywordin = input( '>' )
print ( f'Filtering out {keywordin}...' )

# Gets the html text, "beautifies" it.
html_text = requests.get( f'https://www.zaubacorp.com/companysearchresults/{keywordin}' ).text
soup = BeautifulSoup (html_text, 'lxml')

# Makes an array of the links to various firm pages on ZaubaCorp in href and name inside <a> tag.
firm_links = soup.find_all('a')

# Choice of the user for output txt file
print ("Which of these would you prefer? (Choose 1 or 2, any other choice will exit the program)")
print ("1. Names with Emails")
print ("2. Emails only")
choice = input ('>')

if choice != '1' and choice != '2':
    print ("Exit successful...")

else:
    # 500 firms accessible at a time through the html version
    # 32nd entry has the first firm details
    for i in range (32,532):

    # Uncomment below lines after adding link hit codes
    #    print(firm_links[i]['href'])
    #    print(firm_links[i].text)
        
        # Gets html text for the firm specific website and "beautifies" it
        
        html_text2 = requests.get(firm_links[i]['href']).text
        soup2 = BeautifulSoup(html_text2, 'lxml')

        # To judge activity, hits the <span> tag and checks its 32th entry 
        # (based on a general overview of the site's html code)
        # There are a lot of defunct / listed for exclusion companies on the site
        
        activity_stat = soup2.find_all('span')
        if activity_stat[32].text == 'Active':
            
            # Finds <p> tags and lists them in an array

            email_seq = soup2.find_all('p')

            # Remember there should be an 'a', not a 'w'.
            if choice == '1':
                with open('Name_Email.txt','a') as f:
                    
                    # firm_links[i].text gives the Firm name
                    f.write(f"Firm Name: {firm_links[i].text}"'\n')
                    
                    # Brute force to find the Email ID because its relative location
                    # was variable when seen wrt different firms
                    
                    # To ensure only the first mail is picked
                    count = 0

                    for j in range(0,len(email_seq)):
                        if count < 1:

                            # The string 'Email ID' is present in the text 
                            # for the array element containing the mail address
                            
                            if 'Email ID' in email_seq[j].text:
                                
                                f.write(f"E-mail: {email_seq[j].text.replace('Email ID: ','').split()[0]}"'\n')
                                
                                count = count + 1
            
            if choice == '2':
                with open('Email.txt','a') as f:
                    # To ensure only the first mail is picked
                    count = 0

                    for j in range(0,len(email_seq)):
                        if count < 1:

                            # The string 'Email ID' is present in the text 
                            # for the array element containing the mail address
                            
                            if 'Email ID' in email_seq[j].text:
                                
                                f.write(email_seq[j].text.replace('Email ID: ','').split()[0]+';'+'\n')
                                
                                count = count + 1
                