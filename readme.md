### Just a fun project where I try to find a Russian word in Cyrillic that looks like an English word (using latin alphabet), and pronounced completely diffently.

The Cyrillic (Russian) alphabet intrigues me whenever I see it while travelling, and I caught on what a lot of the letters mean what based on context. For example "Р" is actually an R sound, so "Russia" written in Cyrillic is "Русија" pronounced Russ-ee-ya.

So... I came up with an interesting idea, find a word written in Cyrillic that would look like a completely different sounding existing word in English.

For example the Russian word "нога" looks like "Hora" but it's pronounced noga, and means leg.

But I want something interesting, like synonym or an antonym, whcih I don't end up getting that. Or a word that's longer.

So I made a table with the Cyrillic alphabet (the .csv file) and what closest looking letter to it in the Latin script and awarded "points" based on how much they match the look of a Latin alphabet, and even more points dissimilar the sounds are.

For example the Cyrillic letter "Ш" looks a lot like W so I gave it the maximum points for look, and it's pronounced "sh" which is completely different sounding that "w" so I gave it maximum points sound.

Made that table, downloaded a list of Russian words. Got a list of English words. Made a Python script to go through the Russian words and find similar looking English words.

And gave me the top 100 words. The words' points are based on the sum of its letters' points.

And... There aren't that many good ones. **By far the best one is "щедрой" which looks like "weapon" and it means "generous" in Russian and is pronounced shchedroy.** It got the most points with a 10.95.

It's a one-time run script written to just get the answer.

This can be done for other Cyrillic languages too, but they may have additional letters so the table would need to be expanded for those. And their dictionaries would need to be downloaded.

The same idea can be done for different alphabets versus English too. You are free to expand upon this idea, and use this code.