<h1> Models</h1>

<span id="database"></span>

###  Database
- During the development phase I have worked with the **sqlite3** database, which was set by default by Django. 
- For deployment, I used the **PostgreSQL** database whcih is provided by Heroku. 

<span id="data-modelling"></span>

###  Data Modelling

#### 1. Profile app 
#### UserProfile model

| **Name** | **Database Key** | **Field Type** | **Validation** |
--- | --- | --- | --- 
 User | user | OneToOneField |  User, on_delete=models.CASCADE
 Phone number | default_phone_number | CharField | max_length=20, null=True, blank=True
 Street address 1 | default_street_address1 | CharField | max_length=80, null=True, blank=True
 Street address 2 | default_street_address2 | CharField | max_length=80, null=True, blank=True
 Town/City | default_town_or_city | Charfield | max_length=40, null=True, blank=True
 County | default_county | Charfield | max_length=80, null=True, blank=True
 Postcode | profile_postcode | CharField | max_length=20, null=True, blank=True
 Country | profile_country | CountryField | blank_label='Country', null=True, blank=True
 

#### 2. Products app 
#### Category model

| **Name** | **Database Key** | **Field Type** | **Validation** |
--- | --- | --- | --- 
 name | name | CharField | max_length=254
 Friendly name | friendly_name | CharField | max_length=254, null=True, blank=True

 #### Product model

| **Name** | **Database Key** | **Field Type** | **Validation** |
--- | --- | --- | --- 
 Category| category| ForeignKey | Category, null=True, blank=True, on_delete=models.SET_NULL
 Sku number | sku | CharField | max_length=254, null=True, blank=True
 Name| name | CharField | max_length=254
 Description| description | TextField | null=True, blank=True
 Price | price | DecimalField | max_digits=6, decimal_places=2, null=False, default=0
 Rating | rating | DecimalField | max_digits=6, decimal_places=2, null=False, default=0
 Image | image | ImageField | null=True, blank=True
 Image url | image_url | URLField | max_length=1024, null=True, blank=True

 #### Review model
 
| **Name** | **Database Key** | **Field Type** | **Validation** |
--- | --- | --- | --- 
 user_profile | user_profile | ForeignKey | UserProfile, on_delete=models.SET_NULL,null=True, blank=True,
 Product| product |ForeignKey| Product, null=False, blank=False,on_delete=models.CASCADE,related_name='review'


#### 3. Checkout app 
#### Order model

| **Name** | **Database Key** | **Field Type** | **Validation** |
--- | --- | --- | --- 
 Order number | order_number | CharField | max_length=32, null=False, editable=False
 User profile | user_profile | ForeignKey | UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders'
 Full name | full_name | CharField | max_length=50, null=False, blank=False
 Email| email| EmailField | max_length=254, null=False, blank=False
 Phone number | phone_number | Charfield | max_length=20, null=True, blank=True
 Country| country | CountryField | blank_label='Country *', null=False, blank=False
 Postcode | postcode| CharField | max_length=20, null=True, blank=True
 Town/City | town_or_city | CharField | max_length=40, null=True, blank=True
 Street address 1 | street_address1 | CharField | max_length=80, null=True, blank=True
 Street address 2 | street_address2 | CharField | max_length=80, null=True, blank=True
 Country | profile_country | CountryField | blank_label='Country', null=True, blank=True
 Date | date | DateTimeField | auto_now_add=True
 Delivery cost | delivery_cost | DecimalField | max_digits=6, decimal_places=2, null=False, default=0
 Order total | order_total | DecimalField | max_digits=10, decimal_places=2, null=False, default=0
 Grand total | frand_total | DecimalField | max_digits=10, decimal_places=2, null=False, default=0
 Original bag | original_bag | TextField | null=False, blank=False, default=''
 Stipe pid | stripe_pid | CharField | max_length=254, null=False, blank=False, default=''

 #### OrderLineItem model

| **Name** | **Database Key** | **Field Type** | **Validation** |
--- | --- | --- | --- 
 Order  | order | ForeignKey | CharFieldmax_length=200, unique=True
 Product | product | ForeignKey | Product, null=False, blank=False, on_delete=models.CASCADE
 Quantity | quantity | IntegerField | null=False, blank=False
 Lineitem total | lineitem_total | DecimalField | max_digits=6, decimal_places=2, null=False, blank=False, editable=False


 #### 4. Blog app 

#### Post model
 | **Name** | **Database Key** | **Field Type** | **Validation** |
--- | --- | --- | --- 
 Title  | title | ForeignKey | Order, null=False, blank=False, on_delete=models.CASCADE, related_name='lineitems'
 Slug | slug | ForeignKey | Product, null=False, blank=False, on_delete=models.CASCADE
 Author | author | ForeignKey | UserProfile, on_delete=models.CASCADE
 Updated_on | updated_on |DateTimeField| auto_now=True
 Content | content | TextField | max_length=900, unique=True
 Created_on | created_on |DateTimeField| auto_now_add=True
 Status | status |IntegerField| choices=STATUS, default=0

 #### Comment model
 | **Name** | **Database Key** | **Field Type** | **Validation** |
--- | --- | --- | --- 
 Post  | post | ForeignKey | Post, related_name='comments',on_delete=models.CASCADE)
 Name| name | CharField | max_length=255
 Email| email| EmailField | max_length=254, null=False, blank=False
 Body | body | TextField |
 Date_added | date_added |DateTimeField| auto_now_add=True



- [Back to read me](/README.md)

<div align="right">
    <a href="">To The Top!</a>
</div>