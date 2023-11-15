# darc.ai

Welcome to darc.ai, the AI branch of the non-profit David Attenborough Research Consortium (DARC). We love DA, and therefore we aim to enrich DAs work using modern deep learning and generative AI methods. Those results, together with extracted image frames from videos will constitute the darc-dataset (freely available as huggingface dataset). A dataset that we hope the machine learning and AI community enjoys and plays with.

We will share our initial experimentation on documentary-format video enrichment, understanding and accessible knowledge base building and semantic search here. In one of our first contributions we will attempt to capture DAs unique style of presenting into a german language script of DAs classic "Life on Earth (1979)".

## 1. David Attenboroughs immense productivity over decades

Figure 1 shows the number of major programs DA created across seven and a half decades (n=147, source: https://en.wikipedia.org/wiki/David_Attenborough_filmography). Most often he was credited as writer and presenter (47/147), followed by narrator (n=31), presenter (n=22) and narrator and presenter (n=16) (data not shown). The right hand y-axis (red color) shows the total video duration of the six programs (n=46 videos) we've selected for our initial investigation.

![](readme-examples/fig1.png)


## 2. Video sources and enrichment

Figure 2 illustrates our video data source and enrichment processes applied.

Our video source is the Wildlife Documentaries Collection on archive.org (https://archive.org/download/WildlifeDocumentaries). It is a David Attenborough in The total viewing duration of n=341 MP4 video files was estimated close to 243 hours. Furthermore, 22 hours of audio recordings such as audiobooks, interviews and more is available there.

![img](readme-examples/fig2.png)

The six programs we've selected amount to 44 hours of video material (roughly 18% of the total video material on internet-archive.org) and span from the 60s to the 2020s:

- *1960 - The People of Paradise*
- *1963 - Quest Under Capricorn*
- *1979 - Life on Earth*
- *1995 - The Private Life of Plants*
- *2006 - Planet Earth*
- *2015 - The Hunt*
