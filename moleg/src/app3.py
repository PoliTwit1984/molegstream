import plotly.figure_factory as ff

title = "Most Active #Moleg Tweeters over last 1000 Tweets 5-5-2022"
width = 2000
font_size = 40
data = [
    ["Name", "Username", "Followers", "Tweets"],
    ["🍷 Ozark Wine Club 🇺🇸🗽⚖️", "@jchrthomas", 1539, 77],
    ["Emily Manley", "@EmilyManleyTV", 3424, 50],
    ["House Communications", "@MOHOUSECOMM", 3371, 32],
    ["Rudi  i Keller", "@RudiKellerMI", 5551, 31],
    ["Galen Bacharier", "@galenbacharier", 2453, 27],
]

# ['Jason Hancock', '@J_Hancock', 14669, 20], ['Tessa Weinberg', '@Tessa_Weinberg', 4118, 18], ['robert bucklin🇺🇲', '@robertbucklin8', 393, 17], ['Acceptably Cromulent', '@NoWay14894688', 58, 17], ['Ian Wrobel', '@IanWrobel', 794, 16], [' 'KurtEricksonPD', '@KurtEricksonPD', 8313, 15], ['GovWatch', '@GovWatchLLC', 3155, 15], ['CCRider', '@ES03784893', 1783, 14], ['Missouri Independent', '@MO_Independent', 7528, 14], ['Politwit', '@Politwit1984', 119, 14], ['Kacen J. Bayless', '@Kacen', 1664, 14], ['Show-Me Institute', '@ShowMe', 18858, 12], ['Sue Gibson', '@SheWho_Resists', 2805, 12], ['Joseph Beaudet (they/them)', '@byJosephBeaudet', 202, 11], ['Alisa Nelson', '@alisagbrnelson', 1774, 11], ['Laura B - Meramec Township Committeewoman', '@LauraAnnSTL', 6960, 10], ['Missouri House Democratic Caucus', '@MOLegDems', 10913, 10], ['Senate Democrats', '@MoSenDems', 4388, 10], ['Marina Silva', '@MarinaSilvaKY3', 625, 9], ['eapenthampy', '@eapenthampy', 3203, 8], ['Tavish Misra (he/him) 🇺🇦', '@TavishMisra', 1062, 8], ['Hannah Falcon ABC 17', '@Ha annahFalconTV', 1362, 8]

colorscale = [[0, 'red'],[.5, 'blue'], [.8, 'yellow'], [1, 'green']]
fig = ff.create_table(data, colorscale=colorscale)
fig.update_layout({"margin": {"t": 80}})
fig.update_layout(title_text=title, title_x=0.5)
fig.update_layout(font_size=20)
fig["layout"]["title"]["font"] = dict(size=font_size)
fig.update_layout(width=width)
fig.add_layout_image(
        dict(
            source="flag.jpg",
            xref="x",
            yref="y",
            x=0,
            y=3,
            sizex=2,
            sizey=2,
            sizing="stretch",
            opacity=0.5,
            layer="below")
)



fig.show()
