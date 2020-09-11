import textwrap
from collections import OrderedDict

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
import squarify  # pip install squarify (algorithm for treemap)&lt;/pre&gt;
import seaborn as sns

from mlxtend.frequent_patterns import apriori, association_rules

from io import StringIO
import base64


import numpy as np
import pandas as pd


def treemap_count(
    count_dict,
    question_title=None,
    cmap=matplotlib.cm.Oranges,
    figsize=(20, 9.0),
    output_filename=None,
    format_="pdf"
):
    plt.clf()
    my_values = list(count_dict.values())

    # create a color palette, mapped to these values
    mini = min(my_values)
    maxi = max(my_values)
    norm = matplotlib.colors.Normalize(vmin=mini, vmax=maxi)
    colors = [cmap(norm(value)) for value in my_values]

    # Change color
    fig, ax = plt.subplots(1, figsize=figsize)
    squarify.plot(
        sizes=my_values, label=list(count_dict.keys()), alpha=0.8, color=colors, ax=ax,text_kwargs={"fontsize":16}
    )
    plt.axis("off")
    if question_title:
        plt.title(
            "Occurences des mots du lexique dans les réponses à la question : \n{0}".format(
                question_title
            )
        )
    if output_filename:
        plt.savefig(output_filename, bbox_inches="tight", format=format_ ,transparent=True)
    else:
        plt.show()


def count_barplot(count_dict, question_title=None,figsize=(20,10), output_filename=None,format_="pdf"):
    plt.clf()
    df_count = (
        pd.DataFrame.from_dict(count_dict, orient="index")
        .reset_index()
        .rename(columns={"index": "term", 0: "percent"})
    )
    df_count = df_count.sort_values("percent", ascending=False)
    df_count["percent"]=(df_count.percent/df_count.percent.max())*100
    sns.set_style("dark")
    fig, ax = plt.subplots(1, figsize=figsize)
    sns.barplot(
        data=df_count.head(15),
        x="term",
        y="percent",
        palette=sns.color_palette("Blues_d", n_colors=15),
        ax=ax
    )
    ax.set(xlabel="", ylabel="Pourcentages des réponses")
    ax.set_ylabel("Pourcentages des réponses",fontsize=22)
    ax.tick_params(axis='both', which='major', labelsize=22)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=40, ha="right")
    if question_title:
        ax.set_title(
            "Pourcentages d'apparition des mots-clés dans les réponses à la question :\n {0}".format(question_title),fontdict={"fontsize":"22"}
        )
    ax.set_ylim((0,100))
    if output_filename:
        plt.savefig(output_filename, bbox_inches="tight", format=format_ )
    else:
        plt.show()


def class_plot(count_dict,question_title=None, figsize=(20, 10), labels_dict=None, output_filename=None,format_="pdf"):
    plt.clf()

    def label(xy, text):
        plt.text(xy[0], xy[1], text, ha="center", family="sans-serif", size=22)

    fig, ax = plt.subplots(1, figsize=figsize)
    patches = []

    max_val = np.max(list(count_dict.values()))

    count_dict = OrderedDict(sorted(count_dict.items(), key=lambda t: t[1]))
    i = 0
    for class_, freq in count_dict.items():
        r = ((np.log(freq) / np.log(max_val))) / 2

        plt.plot([i - r, i + r], [r * 2 + 0.01, r * 2 + 0.01], "--", c="black")
        plt.text(
            i, r * 2 + 0.05, f"{freq:,d}", ha="center", family="sans-serif", size=14
        )

        # add a circle
        circle = mpatches.Circle((i, r), r, ec="none")
        patches.append(circle)
        label((i, -0.2), labels_dict[class_] if labels_dict else class_)
        i += 1

    colors = np.linspace(0, 1, len(patches))
    collection = PatchCollection(patches, cmap=plt.cm.tab10)
    collection.set_array(np.array(colors))
    ax.add_collection(collection)

    plt.axis("equal")
    plt.axis("off")
    plt.tight_layout()
    if question_title:
        plt.title("Distribution des classes des mots-clés identifiées dans les réponses à la question : \n{0}".format(question_title),fontdict={"fontsize":"22"})
    if output_filename:
        plt.savefig(output_filename, bbox_inches="tight", format=format_ ,transparent=True)
    else:
        plt.show()


def camenbert_classification(
    df, cols, grid_size, figsize=(20, 20), output_filename=None, format_="pdf"
):
    epsilon =np.finfo(float).eps
    if len(cols) != grid_size[0] * grid_size[1]:
        raise ValueError("Number of columns must fit the grid dimension !")
    wrapper = textwrap.TextWrapper(width=50)
    N = len(df)
    fig1, axs = plt.subplots(*grid_size, figsize=figsize)
    axs = axs.flatten()
    for ix, col in enumerate(cols):
        nb_transport = df[col].sum()
        d = np.array(
            [["Transport", nb_transport /(N+epsilon)], ["Autres", (N - nb_transport) / (N+epsilon)]]
        )
        axs[ix].pie(d[:, 1], labels=d[:, 0], autopct="%1.1f%%", startangle=90)
        axs[ix].set_title("\n".join(wrapper.wrap(col.split(" - ")[-1])))
    plt.axis("off")
    plt.suptitle(
        "Pourcentage de réponses parlant de transport",
        fontsize=28,
        y=0.95,
        fontweight="bold",
    )
    if output_filename:
        plt.savefig(output_filename, bbox_inches="tight", format=format_ ,transparent=True)
    plt.show()


def apriori_plot(bin_occurrences,figsize=(20, 20), output_filename=None, format_="pdf"):
    fig, ax = plt.subplots(1, figsize=figsize)
    freq_items = apriori(bin_occurrences, min_support=0.2, use_colnames=True)
    freq_items.plot.bar(x="itemsets", y="support", ax=ax)
    if output_filename:
        plt.savefig(output_filename, format=format_ ,transparent=True)
    plt.show()

def get_base64_img_from_buffer(buffer, class_="", id_=""):
    code_64 = base64.encodestring(buffer.getvalue())
    return """<img src="data:image/png;base64,{0}" class="{1}" id="{2}" />""".format(
        d, class_, id_
    )


################## INTERACTIVE PLOT IS GOOOOOOOD ! ###########

import plotly.express as px
import plotly
def treemap_interactive(count_dict,lexique,lexique_class_labels):
    df_viz = pd.DataFrame(count_dict.items(),columns=("word","freq"))
    class_dict = dict(lexique["word class".split()].values)
    if lexique_class_labels:
        df_viz["class"] = df_viz.word.apply(lambda x:lexique_class_labels[class_dict[x]])
        fig = px.treemap(df_viz, path=["class",'word'], values='freq')
    else:
        fig = px.treemap(df_viz, path=['word'], values='freq')
    return fig

def sunburst_interactive(count_dict,lexique,lexique_class_labels):
    df_viz = pd.DataFrame(count_dict.items(),columns=("word","freq"))
    class_dict = dict(lexique["word class".split()].values)
    if lexique_class_labels:
        df_viz["class"] = df_viz.word.apply(lambda x:lexique_class_labels[class_dict[x]])
        fig = px.sunburst(df_viz, path=["class",'word'], values='freq')
    else:
        fig = px.sunburst(df_viz, path=['word'], values='freq')
    return fig

def count_barplot_interactive(count_dict):
    df_viz = pd.DataFrame(count_dict.items(),columns=("word","freq")).sort_values(by="freq",ascending=False)
    fig = px.bar(df_viz, x='word', y='freq',labels={"word":"Mot-clé","freq":"Nombre de réponses"})
    return fig

def get_html_from_plotly(fig):
    return plotly.offline.plot(fig,output_type="div",include_plotlyjs=False)

#get_html_from_plotly(treemap_interactive(count_dict,lexiques[lex],lexique_class_labels[lex]))