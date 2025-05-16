                    # elif "latest news" in query:

                    #     newsapi = NewsApiClient(api_key='4dbc17e007ab436fb66416009dfb59a8')
                    #     speak("enter the country below..")
                    #     input_country = takeCommand()
                    #     input_countries = [f'{input_country.strip()}']
                    #     countries = {}

                    #     for country in pycountry.countries:
                    #         countries[country.name] = country.alpha_2

                    #     codes = [countries.get(country.title(), 'Unknown code')
                    #              for country in input_countries]

                    #     speak("which category are you interested in? there is a list given below input any one...")
                    #     option = takeCommand()
                    #     top_headlines = newsapi.get_top_headlines(category=f'{option.lower()}', language='en',
                    #                                               country=f'{codes[0].lower()}')

                    #     Headlines = top_headlines['articles']

                    #     if Headlines:
                    #         for articles in Headlines:
                    #             b = articles['title'][::-1].index("-")
                    #             if "news" in (articles['title'][-b + 1:]).lower():
                    #                 print(f"{articles['title'][-b + 1:]}: {articles['title'][:-b - 2]}.")
                    #             else:
                    #                 result = f"{articles['title'][-b + 1:]} News: {articles['title'][:-b - 2]}."
                    #                 speak(result)
                    #                 print(f"{articles['title'][-b + 1:]} News: {articles['title'][:-b - 2]}.")
                    #     else:
                    #         print(f"Sorry no articles found for {input_country}, Something Wrong!!!")

