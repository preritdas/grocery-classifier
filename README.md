![tests](https://github.com/preritdas/grocery-classifier/actions/workflows/pytest.yml/badge.svg)

**Note: this repo is no longer maintained *here*. It's part of my "Personal API" project, so all updates and developments happen in the "groceries" applet of the API.**

# Grocery Classification

Only one lap around the grocery store...

![class](readme-content/class.jpeg)

## Formatting guidelines

There really aren't any. Just a couple things to be aware of to avoid crashing the classification algorithm. 

- Don't used dashed lists. 
- New line for each item.
- Quantities go at the beginning, in numeric form. They are optional.
- Add special options in parenthesis, ex. `3 apples (the good ones)`
- Setup is optional. It efficiently reorders the categories based on store layout. Create a setup manually in [setups.json](setups.json).
  - Setup line is case insensitive
  - Line between setup and content is unnecessary

That's all. Here's a sample...

```text
setup: whole foods

8 bananas
1 blueberry
1 whole milk
1 whole lactaid
1 2% lactaid
Snacks (good stuff)
Shaving foam (red Gillette)
Whole wheat bread
```


## Deployment

It's a REST API built with Flask and the Nexmo API. Nexmo posts the inbound sms, the API handles it and texts back a classified grocery list. You'll have to deploy it with a `keys.ini` file with Nexmo contents, expose the port with ngrok or socketxp or something, then give that endpoint to Nexmo.
