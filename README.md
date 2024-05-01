# Horizon Markets

## Purpose of the Project

**Description:**

Welcome to Horizon Markets! Horizon Markets is a web-based cryptocurrency exchange designed to empower users with comprehensive tools for trading and analysis. With support for over 152 cryptocurrencies, users can seamlessly navigate through the platform to explore, chart, analyze, and execute trades with ease. Our priority lies in providing a secure environment for transactions, ensuring the safety and convenience of deposits and withdrawals through over 5 supported payment methods.

**Favourite Coins:** 

Horizon Markets introduces the feature to favorite specific cryptocurrencies, enhancing the user experience by enabling direct access to price information for these chosen coins from their dashboard. This functionality equips users with up-to-date insights, empowering them to make informed decisions and improve their trading performance.

**Advanced Charting:** 

Our platform offers advanced charting capabilities, allowing users to stack up to three advanced TradingView widget charts on the charts page. This facilitates in-depth analysis as users can compare different time frames or cryptocurrencies simultaneously. This feature is instrumental in providing users with comprehensive insights into market trends, aiding them in making strategic trading decisions.

**Execute Trades:** 

Horizon Markets is equipped with advanced trading features tailored to accommodate various trading styles and preferences. Users can utilize functionalities such as limit and market orders, stop-loss and take-profit integration, and a quick-close button to efficiently manage their positions. These features empower users to execute trades with precision and agility, enhancing their overall trading experience on our platform.

### Why This Project:

At Horizon Markets, our project aims to revolutionize cryptocurrency trading by providing a user-centric platform equipped with cutting-edge features and functionalities. We empower traders of all levels with comprehensive tools, allowing them to view, chart, and analyze over 152 supported cryptocurrencies while executing trades seamlessly. Our platform enhances user experience by streamlining the trading process, offering advanced charting capabilities for in-depth analysis, and prioritizing security and convenience with secure transaction processes and multiple payment methods. With tailored trading features such as limit and market orders, stop-loss and take-profit integration, and a quick-close button, Horizon Markets caters to diverse trading styles and preferences. Join us and experience the future of cryptocurrency trading today!

### Project Objectives:

- *Secure and Seamless Registration:* Incorporate Django's built-in OAuth system to enable users to register and log in securely with seamless integration. Enable users to modify their account credentials to rectify any inaccuracies or mistakes in their information.

- *Secure Transaction Processes:* Integrate the APIs of Stripe and PayPal to facilitate various payment and withdrawal options, ensuring flexibility for users.

- *Comprehensive Charting:* Develop a system that enables users to access and manage up to three charts simultaneously, each equipped with diverse charting features to enhance cryptocurrency analysis capabilities.

- *Advanced Trading:* Implement an intuitive and responsive trading interface that empowers users to execute trades efficiently and effectively, incorporating advanced order types, real-time market data, and customizable trading strategies to optimize their trading experience.

- *Customer-Support System:* Establish a customer support system that provides assistance to user inquiries and issues, utilizing Django's built in mail protocall.

## User Stories

### Current User Stories:

1. **As a new user**, As a cryptocurrency trader, I want to be able to easily register for an account on Horizon Markets through OAuth integration, so that I can quickly access the platform. 

2. **As a seasoned investor**, I want the ability to customize my dashboard on Horizon Markets by favoriting specific cryptocurrencies, so that I can easily track their prices and performance without having to search through a long list of coins.

3. **As a technical analyst**, I want access to advanced charting features on Horizon Markets, such as the ability to stack up to three different charts with various timeframes and indicators, so that I can conduct in-depth analysis and make well-informed trading decisions.

4. **As a security-conscious user**, I want Horizon Markets to offer multiple payment and withdrawal methods, including integration with reputable payment processors like Stripe and PayPal, so that I can choose the most convenient and secure option for managing my funds on the platform.

5. **As a novice trader**, I want Horizon Markets to provide a user-friendly trading interface with intuitive features like limit and market orders, stop-loss and take-profit options, and a quick-close button, so that I can easily execute trades and manage my positions without feeling overwhelmed by complex trading terminology.

### Future User Stories:

1. **As a high-volume trader**, I want Horizon Markets to introduce a VIP or premium membership program with exclusive benefits such as reduced trading fees, priority customer support, and access to advanced trading tools and analytics, to incentivize loyalty and attract more active traders to the platform.

2. **As a global trader**, I want Horizon Markets to expand its supported languages beyond English to cater to a more diverse user base, ensuring that non-English speaking users can navigate the platform and access support resources in their preferred language.

3. **As a trader interested in diversifying my portfolio**, I want Horizon Markets to introduce support for trading derivatives such as futures contracts and options, so that I can hedge my positions and take advantage of price movements in the cryptocurrency market.

## Features

### Key Features:

- **Registration:** Allows users to become members of the website, disabling any incorrect inputs.
![Registration Screenshot](static/images/readme-images/registration.png)

- **Log-In:** Allows users to enter their individual accounts, validating information and displaying error messages if any of the information is incorrect.
![Log In Screenshot](static/images/readme-images/login.png)

- **Navigation:** Easy-to-use navigation for a seamless user experience while navigating the website. This feature displays navigation links, guiding you to each individual section of the website, along with the settings page and log-out button.
![Navigation Screenshot](static/images/readme-images/navigation.png)

- **Dashhboard:** Displays the user's account history information, along with live price updates and details about their favorite cryptocurrency coins.
![Dashboard Screenshot](static/images/readme-images/dashboard.png)

- **Markets:** Showcases the price action of any cryptocurrency through simple charts, while also offering the ability to favorite cryptocurrencies.
![Markets Screenshot](static/images/readme-images/markets.png)

- **Chart:** Users can view and analyze up to a total of three advanced charts simultaneously, across any chosen cryptocurrency and time frame.
![Chart Screenshot](static/images/readme-images/chart.png)


- **Trade:** Enables users to trade any cryptocurrency, offering features such as limit and market orders, stop-loss, and take-profit options. Additionally, it displays current positions and relevant information, along with a summary of today's trades.
![Trade Screenshot](static/images/readme-images/trade.png)

- **Settings:** Includes a customer support section where users can reach out for technical assistance, as well as the ability to update their current user profile information.
![Settings Screenshot](static/images/readme-images/settings.png)

- **Deposits:** Allows users to securely deposit funds into their account using Stripe's payment processes.
![Deposits Screenshot](static/images/readme-images/deposits.png)

- **Withdrawals:** Allows users to securely withdraw funds from their account using PayPal's payment processes.
![Withdrawals Screenshot](static/images/readme-images/withdrawals.png)

- **Transactions:** Showcases all trades executed, providing comprehensive information about each trade.
![Transactions Screenshot](static/images/readme-images/transactions.png)

## Future Features

### Planned Future Features:

- Implement additional currency pairs, starting with GBP (British Pound) and EUR (Euro), to provide users with more trading options.
- Implement margin trading functionality, allowing users to borrow funds to leverage their positions and potentially increase their returns (while also increasing their risk).
- Introduce a premium membership program with exclusive benefits such as reduced trading fees.

## User Experience Design Features

### Typography:

- **Primary Font:**  *Poppins*, Poppins is a widely used font known for its modern, clean appearance and high readability. Its balanced proportions and consistent letterforms make it suitable for this web-application. Available in multiple weights and styles, Poppins offers versatility for different typographic needs, supporting both headlines and body text. Additionally, its international support and accessibility features, such as open counters and ample spacing, cater to diverse audiences and ensure readability across languages and user groups. Poppins is also favored for branding purposes due to its contemporary yet neutral aesthetic, helping maintain brand consistency across different platforms and communications. Overall, Poppins is valued for its contemporary design, readability, versatility, and accessibility, making it a personal choice.

- **Secondary Font:** *Sans-Serif*, I chose sans-serif as my secondary font because it is a basic font that is universally supported across all browsers. In the event that my main font fails to load for any reason, I can rely on and depend on sans-serif as a fallback option.

### Color Scheme:

- **Primary Color:**  *#437DBC*, Using the color #437DBC in UI and UX design offers several advantages. Its deep blue hue with a hint of cyan creates a visually appealing palette, drawing users' attention and enhancing engagement. Additionally, the color conveys professionalism and trustworthiness, making it suitable for trading interfaces. Its clear contrast against light backgrounds improves readability and ensures key elements stand out.
  
- **Secondary Color:** *#93B8E1* Using the color #93B8E1 as a secondary color in UI and UX design offers several benefits. Its soft and muted blue tone creates a calming and soothing effect, complementing primary colors and enhancing the overall color palette. As a secondary color, #93B8E1 can be used for accents, highlights, or background elements, providing visual interest without overpowering the primary content. Its gentle hue promotes a sense of harmony and balance in the interface, contributing to a cohesive and pleasant user experience. Additionally, #93B8E1 maintains good contrast against darker or lighter tones, ensuring readability and accessibility.

## Wireframes

### Wireframes:

- **Dashboard Wireframe:** ![Dashboard Wirerame Screenshot](static/images/wireframes/dahsboard-wireframe.png)

- **Markets Wireframe:** ![Markets Wirerame Screenshot](static/images/wireframes/markets-wireframe.png)

- **Chart Wireframe:** ![Chart Wirerame Screenshot](static/images/wireframes/chart-wireframe.png)

- **Trade Wireframe:** ![Trade Wirerame Screenshot](static/images/wireframes/trade-wireframe.png)

## Technologies

### Languages:

- **HTML:** Used to structure the contents for my website.
- **CSS:** Used to style the content of my website.
- **JavaScript:** Used to add the interactivity to the elements.
- **Python:** Used for the back-end and data management.
- **Sqlite:** Used as the database for the website.

**Frameworks and Add-Ons:**

- **Django:** Web Developent framework for Python.
- **Bootstrap:** Used to make the website scalable across multiple screen sizes.
- **Chart.js:** Used to create the graphs on my website.
- **Stripe API:** Used for secure deposits.
- **PayPal API:** Used for secure Withdrawals.
- **Binance Websocket and  API:** Used for trading information and execution of trades.
- **TradingView API:** Used for charting and displaying markets.
- **Google Fonts:** Used to apply non-included fonts onto my text.

**Additional:**

- **GitPod:** My Integrated Development Environment.
- **Git and Github:** Used Git for source code management and github for version control.
- **Heroku:** For deployment of my website.
- **ElephantSQL:** Cloud-based PostgreSQL database service that I used to host my database.

## Testing

### W3C Validator:

- ***HTML*** ![HTML Passing Validator Screenshot](static/images/readme-images/w3c-css-validator.png)

### W3C CSS Validator:
- ***CSS*** ![CSS Passing Validator Screenshot](static/images/readme-images/w3c-css-validator.png)

### JSHint:
- ***JavaScript*** ![Javascript Passing Screenshot](static/images/readme-images/jshint-js-validator.png)


### JSHint:
- ***Python*** ![Python Passing Screenshot](static/images/readme-images/w3c-css-validator.png)

### Manual Testing:

| Feature                      | Action                                | Expected Result                    | Tested | Passed  | Comments   |
| ---------------------------- | ------------------------------------- | ---------------------------------- | ------ | ------- | ---------- |
| Site Navigation              | Click on the links in the navigation  | Redirect to relevant part of site  | ✅     | ✅     | Works Fine |
| Log Out button               | Click on the 'Log Out' Button         | Redirect to confirmation page      | ✅     | ✅     | Works Fine |
| Transfer button              | Click on the 'Transfer' Button        | Redirect to Deposits page          | ✅     | ✅     | Works Fine |
| Settings button              | Click on the 'Settings' Button        | Redirect to Settings page          | ✅     | ✅     | Works Fine |
| Withdraw Button              | Click on the 'Withdraw' button        | Redirect to Withdraw form page     | ✅     | ✅     | Works Fine |
| Transaction forms            | Fill transaction form out and submit  | Processes transaction and operates | ✅     | ✅     | Works Fine |
| Registration form            | Fill register form out and submit     | If fields not empty it redirects   | ✅     | ✅     | Works Fine |
| Log In Page Form             | Fill Log In form out and submit       | If fields not empty it redirects   | ✅     | ✅     | Works Fine |
| Account History Chart        | Dispalys all transactions             | Dispalys all queried transactions  | ✅     | ✅     | Works Fine |
| Account History Buttons      | Click on the any of the 3 Buttons     | Dispalys relevant info on chart    | ✅     | ✅     | Works Fine |
| Favourited Crypto Buttons    | Click on the "x" buttons on a crypto  | Removes Crypto and info from list  | ✅     | ✅     | Works Fine |
| Markets Search Bar           | Type a crypto pair into the search    | Displays a simple crypto chart     | ✅     | ✅     | Works Fine |
| Markets Favourite Button     | Click on the heart shaped button      | Adds crypto pair to favourites     | ✅     | ✅     | Works Fine |
| Charts, Interactive Charts   | Click, Select and Drag on Charts      | Should be responsive and functional| ✅     | ✅     | Works Fine | 
| Charts Add Button            | Click on the "+" Button               | Should add another chart if ch > 3 | ✅     | ✅     | Works Fine |
| Chart Remove Button          | Click on the "x" Button               | Should remove chart if chart < 0   | ✅     | ✅     | Works Fine |
| Trade Markets Form           | Fill out form and place trade         | Should open trade position         | ✅     | ✅     | Works Fine |
| Trade Open Position          | Place a trade to see                  | Displays open trading positions    | ✅     | ✅     | Works Fine |
| Trade Close Open Position    | Click on the "x" button in a trade    | Should close the position          | ✅     | ✅     | Works Fine |
| Todays trades                | Close open positions from today       | Displays relevant trade info       | ✅     | ✅     | Works Fine |
| Customer Support             | Click and fill out the form           | Sends an email to admin with info  | ✅     | ✅     | Works Fine |
| User Profile Form            | Click and fill out the form           | Updates user profile information   | ✅     | ✅     | Works Fine |
| Trading Logs Button          | Click on "Trading Logs" button        | redirects to trading logs page     | ✅     | ✅     | Works Fine |
| Account Transactions Button  | Click on "Account Transactions" button| redirects to Account Transactions  | ✅     | ✅     | Works Fine |

### Fixed Bugs:

1. **Trade Entry Calculation:** 
Discovered a bug with the trade entry calculation where I overlooked using the cumulative quote quantity. Realized my mistake was failing to divide the cumulative quote quantity by the quantity of the asset traded to determine the entry price accurately. Corrected the mistake by implementing the proper calculation logic `float(result.get('cummulativeQuoteQty')) / float(result.get('executedQty')))`, dividing the cumulative quote quantity by the asset quantity to obtain the correct trade entry price.

### Supported Screen Sizes:

- **For Small, Medium and Large Phone Screen Sizes:** (Breakpoint: 320px to 576px).
- **For Small and Medium Tablet Sizes:** (576px to 768px).
- **For Small and Medium Laptop Screen Sizes:** (768px to 992px).
- **For Large Laptop and Small Desktop Screen Sizes:** (992px to 1200px).
- **For Large Desktop Screen Sizes:** (1200px +).

### Database Schema:

The Horizon Markets database encompasses several interconnected models designed to manage various aspects of the trading platform. At the core of the database is the `UserProfile` model, which stores user-specific information such as account balance and deposit amount multiplier. The `AccountHistory` model tracks changes in user account balances over time, linking each entry to a user profile through a foreign key relationship. The `Market` model allows users to customize their trading experience by specifying favorite tickers and market preferences, while the `Chart` model enables users to view and analyze multiple cryptocurrency charts simultaneously. The `OpenTrade` model records details of users' open trades, including order type, quantity, and entry price, with each trade associated with a user profile. Additionally, the `TradeHistory` model logs past trades made by users, capturing essential information such as trade date, symbol, and net profit or loss. These models are interconnected through foreign key relationships, facilitating data retrieval and ensuring data integrity across different components of the platform. This schema provides a comprehensive framework for managing user profiles, trading activity, and market preferences within the Horizon Markets application.

## Deployment

To deploy the site, I first created an instance of my database in ElephantSQL. Then, in my IDE, I created a requirements.txt file listing all libraries, frameworks, and add-ons I have used. Following that, I created a Procfile with the commands needed to run my web app. Finally, on Heroku, I added all my environment variables and deployed my site.

The Site was Deployed on Heroku. This is the link <https://my-finview-15e37362d8a7.herokuapp.com/>