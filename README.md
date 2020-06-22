

## Improved Initiative Converter

After discovering the amazing [Improved Initiative](https://www.improved-initiative.com) tool, I created a number of custom creatures for my campaign. Among those were a few I wanted to print and share with my players, as well as view in slightly easier formats. I also wanted to avoid creating homebrew in two places every time, and in classic procrastinating-into-productivity style, I decided to learn enough Python to write a script for it.

Currently, this script has support for Creatures, Characters, and Spells from Improved Initiative, though I'm working on parsing the formatting for PersistentCreatures/Characters. It converts into [Homebrewery](https://homebrewery.naturalcrit.com/) monster stat block style by default, though you can also specify the wide statblock through the **markdown_format** parameter in your commandline. 

Of course, the markdown is also just openable and useable elsewhere - in particular, I really like how it looks in the Engwrite theme in Typora!

Huge credit to NaturalCrit, who made Homebrewery; Evan Bailey and the other Improved Initiative contributors; and [ianjsikes](https://gist.github.com/ianjsikes/1aedfd113243d9cfe69c3b445f1cb562), who originally wrote a nodejs script with similar intent that gave me this idea.

## How to Use

1. Download the package to wherever you want.

2. In the console, run:

   `python II_CONVERTER_PATH INPUT_FILE_PATH `

   For  example, I could run the converter from within `\improved_initiative_converter\` on an Improved Initiative JSON in the same directory like so:

   `python ii_converter improved-initiative.json`

   Optional parameters are **markdown_format** , **overwrite** and **filter**. **Markdown_format** defaults to standard Homebrewery, though wide is also an option. **Overwrite** defaults to false, and the script will ask you for each existing file whether you want to overwrite it or provide a different filename; if set to true, it will overwrite all files by default.  **Filter** defaults to false, and the converter will apply to all records in the input file. If set to true, it will allow you to choose from supported types like `creature, spell, character` or you can pop your JSON open and grab the key of specific records - for example, you could just supply `Creatures.06cn7p2u` and convert a single entity.

   Here's an example of running with config:

   `python ii_converter improved-initiative.json --markdown_format=homebrewery_wide --overwrite=true --filter=true` 

3. All done! Find your files in a `converted` folder at the same directory as your input file, and you can paste them into Homebrewery or wherever you like.

## Common Issues

### How do I get the Improved Initiative JSON file?

To export your homebrew entities from Improved Initiative, go to Settings->Account->Export your user data as JSON file.

### My input filepath is truncating. What's wrong?

If your input filepath includes spaces, wrap the whole thing as a string so argparse recognizes it properly:

`python ii_converter "C:\D and D\Improved Initiative\improved-initiative.json" `

### Why are some records getting skipped as strings?

Currently, some records exported by Improved Initiative are stored as strings that don't parse easily with `json.loads` into JSON. I'll likely add support for these later, but for now, they get skipped. Only Persistent records and Encounters seem to be packaged this way, so far as I checked.

### 'homebrewery_wide' conversions aren't displaying right - they run off the page.

This is a problem with your browser. Homebrewery is built for Chrome, so there can be some display issues on other browsers - for example, I've run into this issue on Firefox. It should work on Chrome, or maybe this will be fixed at a later date.

## Additional Questions/Concerns

Like I mentioned, this is my first ever Python project, so if there's anything going awry, you want to make changes, you vastly improve it, there's something already out there that does this, etc. just let me know! Thank you!

#### Examples

Here's a few demos of the converter in progress, from Improved Initiative to commandline to Homebrewery.

![Demo in Improved Initiative](../assets/improvedinitiative_ex.PNG?raw=true)

![Demo Commandline](../assets/commandline_ex.PNG?raw=true)

![Demo in Homebrewery](../assets/homebrewery_ex.PNG?raw=true)

![Demo in Homebrewery Wide](../assets/homebrewery_wide_ex.png?raw=true)

![Demo in Markdown Editor](../assets/md_editor_ex.PNG?raw=true)