<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00ADD8,100:5A3E85&height=200&section=header&text=Nikita%20Belyakov&fontSize=52&fontColor=ffffff&fontAlignY=34&desc=Go%20Platform%20Engineer&descAlignY=54&descSize=20" width="100%" alt="Nikita Belyakov — Go Platform Engineer"/>

<div align="center">

<a href="https://git.io/typing-svg"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=23&pause=1200&color=00ADD8&center=true&vCenter=true&width=680&height=45&lines=Internal+developer+platforms;Service+mesh+%26+runtime+traffic+control;DBaaS+%E2%80%94+100%2B+clusters%2C+days+to+minutes;MCP+infrastructure+for+AI+coding+agents" alt="Typing SVG" /></a>

<br><br>

[![Website](https://img.shields.io/badge/hexarch.ru-0B0B0B?style=for-the-badge&logo=hexo&logoColor=00ADD8)](https://hexarch.ru)
[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/nikitabelekov)
[![Email](https://img.shields.io/badge/Email-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:nikitabelekov@gmail.com)
![Location](https://img.shields.io/badge/Uzbekistan%20%C2%B7%20UTC%2B5-2E7D32?style=for-the-badge&logo=googlemaps&logoColor=white)
![Open to work](https://img.shields.io/badge/Open%20to%20remote%20work-00ADD8?style=for-the-badge&logo=statuspage&logoColor=white)

</div>

---

## 👋 About

I build **internal developer platforms** — the layer that lets product teams ship
without each of them reinventing networking, databases and tooling.

Currently on the IDP platform team at **VK**: service mesh consolidation across
the holding, runtime traffic control, and the platform's MCP layer that puts
internal infrastructure behind AI coding agents.

Information Security at ITMO, CTF competitor (attack–defense, HackTheBox) — the
security habit shows up in how I design auth and platform boundaries, not only
in the degree.

<br>

## 🛠 What I work on

<table>
<tr>
<td width="50%" valign="top">

### 🕸 Service mesh & traffic control

Consolidated separate mesh solutions into one platform offering — a service
onboards through a single action. Rate limiting, timeouts and circuit breakers
reconfigurable **at runtime**, without a redeploy.

</td>
<td width="50%" valign="top">

### 🗄 DBaaS

Database cluster provisioning with full lifecycle management and an SDK that
ships metrics out of the box. **100+ clusters** for product teams — provisioning
went from days to minutes.

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🤖 AI / agent infrastructure

An MCP Gateway aggregating per-domain MCP servers: stateless with Redis-backed
sessions, **BM25** multilingual tool search, OAuth scope-based authorization,
and clients for Claude Code, Codex and OpenCode.

</td>
<td width="50%" valign="top">

### ⚡ High-load product backends

A **2M+ MAU** service in the VK Health ecosystem on a DDD architecture, with
ClickHouse analytics pipelines behind it.

</td>
</tr>
</table>

<br>

## 🧰 Stack

<div align="center">

![Go](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![C](https://img.shields.io/badge/C-A8B9CC?style=for-the-badge&logo=c&logoColor=black)
![Swift](https://img.shields.io/badge/Swift-F05138?style=for-the-badge&logo=swift&logoColor=white)

![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white)
![Consul](https://img.shields.io/badge/Consul-F24C53?style=for-the-badge&logo=consul&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Temporal](https://img.shields.io/badge/Temporal-000000?style=for-the-badge&logo=temporal&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![ClickHouse](https://img.shields.io/badge/ClickHouse-FFCC01?style=for-the-badge&logo=clickhouse&logoColor=black)
![Redis](https://img.shields.io/badge/Redis-FF4438?style=for-the-badge&logo=redis&logoColor=white)
![Kafka](https://img.shields.io/badge/Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white)
![NATS](https://img.shields.io/badge/NATS-27AAE1?style=for-the-badge&logo=natsdotio&logoColor=white)
![gRPC](https://img.shields.io/badge/gRPC-244B5A?style=for-the-badge&logo=grpc&logoColor=white)

</div>

<br>

## 📌 Projects

<table>
<tr>
<td width="50%" valign="top">

#### [porovnu](https://github.com/HexArchy/porovnu)
![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)
![Swift](https://img.shields.io/badge/SwiftUI-F05138?style=flat-square&logo=swift&logoColor=white)
![Live](https://img.shields.io/badge/live-porovnu.hexarch.ru-2E7D32?style=flat-square)

Free bill splitter. Event-driven Go microservices with a SwiftUI client, running
in production.

</td>
<td width="50%" valign="top">

#### [itmo-calendar](https://github.com/HexArchy/itmo-calendar)
![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)
![CalDAV](https://img.shields.io/badge/CalDAV-5A3E85?style=flat-square)

CalDAV service that syncs university schedules straight into Apple Calendar,
Google Calendar and anything else that speaks CalDAV.

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### [goimporter](https://github.com/HexArchy/goimporter)
![Go](https://img.shields.io/badge/Go-00ADD8?style=flat-square&logo=go&logoColor=white)
![CLI](https://img.shields.io/badge/dev--tool-444?style=flat-square)

Universal Go import organizer — deterministic grouping and ordering of imports
across a codebase.

</td>
<td width="50%" valign="top">

#### [onec-conf-fetcher](https://github.com/HexArchy/onec-conf-fetcher)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Security](https://img.shields.io/badge/offensive--security-B71C1C?style=flat-square)

NetExec module for collecting 1C Enterprise configuration files from Windows
targets over SMB.

</td>
</tr>
</table>

<br>

## 📊 Activity

<div align="center">

<img src="https://github-readme-activity-graph.vercel.app/graph?username=HexArchy&theme=github-compact&hide_border=true&color=00ADD8&line=00ADD8&point=5A3E85&area=true&custom_title=Contributions" width="98%" alt="Contribution activity"/>

</div>

<br>

## 🎓 Background

**ITMO University** — Information Security, 2021–2026
CTF: attack–defense, HackTheBox

I write about architecture at **[hexarch.ru](https://hexarch.ru)**.

<br>

<div align="center">

### 💬 Open to remote work worldwide — [get in touch](mailto:nikitabelekov@gmail.com)

</div>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:5A3E85,100:00ADD8&height=120&section=footer" width="100%" alt=""/>
