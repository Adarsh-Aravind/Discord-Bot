import discord
from discord.ext import commands
import urllib.request
import json
from datetime import datetime
import pytz

class F1Command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.base_url = "https://api.jolpi.ca/ergast/f1/current"
        self.headers = {"User-Agent": "BitBot/1.0"}

    def _fetch_data(self, endpoint):
        req = urllib.request.Request(f"{self.base_url}/{endpoint}", headers=self.headers)
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"Error fetching {endpoint}: {e}")
            return None

    def _get_driver_standings(self):
        data = self._fetch_data("driverStandings.json")
        try:
            standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
            return standings[:10] # Top 10
        except (KeyError, IndexError):
            return []

    def _get_constructor_standings(self):
        data = self._fetch_data("constructorStandings.json")
        try:
            standings = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
            return standings[:10] # Top 10
        except (KeyError, IndexError):
            return []

    def _get_next_race(self):
        data = self._fetch_data("next.json")
        try:
            race = data['MRData']['RaceTable']['Races'][0]
            # Parse UTC time and convert to IST
            utc_time_str = f"{race['date']}T{race['time']}"
            utc_dt = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%SZ")
            utc_dt = pytz.utc.localize(utc_dt)
            ist_dt = utc_dt.astimezone(pytz.timezone('Asia/Kolkata'))
            
            return {
                "name": race['raceName'],
                "circuit": race['Circuit']['circuitName'],
                "circuit_id": race['Circuit']['circuitId'],
                "date": ist_dt.strftime("%d %B %Y at %I:%M %p IST")
            }
        except (KeyError, IndexError):
            return None

    def _build_driver_embed(self, standings):
        desc = ""
        for s in standings:
            desc += f"**{s['position']}.** {s['Driver']['givenName']} {s['Driver']['familyName']} - {s['points']} pts\n"
        return desc if desc else "No driver standings available yet."

    def _build_constructor_embed(self, standings):
        desc = ""
        for s in standings:
            desc += f"**{s['position']}.** {s['Constructor']['name']} - {s['points']} pts\n"
        return desc if desc else "No constructor standings available yet."

    def _get_circuit_image_url(self, circuit_id):
        # A mapping of common circuit IDs to official track layout images
        base_url = "https://media.formula1.com/image/upload/f_auto/q_auto/v1677244985/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9"
        circuit_images = {
            "bahrain": f"{base_url}/Bahrain_Circuit.png",
            "jeddah": f"{base_url}/Saudi_Arabia_Circuit.png",
            "albert_park": f"{base_url}/Australia_Circuit.png",
            "suzuka": f"{base_url}/Japan_Circuit.png",
            "shanghai": f"{base_url}/China_Circuit.png",
            "miami": f"{base_url}/Miami_Circuit.png",
            "imola": f"{base_url}/Emilia_Romagna_Circuit.png",
            "monaco": f"{base_url}/Monaco_Circuit.png",
            "villeneuve": f"{base_url}/Canada_Circuit.png",
            "catalunya": f"{base_url}/Spain_Circuit.png",
            "red_bull_ring": f"{base_url}/Austria_Circuit.png",
            "silverstone": f"{base_url}/Great_Britain_Circuit.png",
            "hungaroring": f"{base_url}/Hungary_Circuit.png",
            "spa": f"{base_url}/Belgium_Circuit.png",
            "zandvoort": f"{base_url}/Netherlands_Circuit.png",
            "monza": f"{base_url}/Italy_Circuit.png",
            "baku": f"{base_url}/Baku_Circuit.png",
            "marina_bay": f"{base_url}/Singapore_Circuit.png",
            "americas": f"{base_url}/USA_Circuit.png",
            "rodriguez": f"{base_url}/Mexico_Circuit.png",
            "interlagos": f"{base_url}/Brazil_Circuit.png",
            "vegas": f"{base_url}/Las_Vegas_Circuit.png",
            "losail": f"{base_url}/Qatar_Circuit.png",
            "yas_marina": f"{base_url}/Abu_Dhabi_Circuit.png"
        }
        return circuit_images.get(circuit_id, "https://media.formula1.com/image/upload/f_auto/q_auto/v1677244985/content/dam/fom-website/2018-redesign-assets/Circuit%20maps%2016x9/Australia_Circuit.png")


    @commands.command(name="f1next")
    async def f1_next(self, ctx):
        async with ctx.typing():
            next_race = self._get_next_race()
            if not next_race:
                await ctx.send("Could not retrieve next race info.")
                return

            embed = discord.Embed(title=f"🏎️ {next_race['name']}", color=discord.Color.red())
            
            race_info = f"**Circuit:** {next_race['circuit']}\n**Time:** 📅 {next_race['date']}"
            embed.description = race_info
            
            image_url = self._get_circuit_image_url(next_race['circuit_id'])
            embed.set_image(url=image_url)
            
            current_year = datetime.now().year
            embed.set_footer(text=f"Note: The displayed circuit layout may vary from current {current_year} FIA Formula 1 regulations")

            await ctx.send(embed=embed)

    @commands.command(name="f1dri")
    async def f1_drivers(self, ctx):
        async with ctx.typing():
            standings = self._get_driver_standings()
            embed = discord.Embed(title="🏎️ F1 Driver Standings", description=self._build_driver_embed(standings), color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(name="f1con")
    async def f1_constructors(self, ctx):
        async with ctx.typing():
            standings = self._get_constructor_standings()
            embed = discord.Embed(title="🏎️ F1 Constructor Standings", description=self._build_constructor_embed(standings), color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(name="f1")
    async def f1_all(self, ctx):
        async with ctx.typing():
            drivers = self._get_driver_standings()
            constructors = self._get_constructor_standings()
            next_race = self._get_next_race()

            embed = discord.Embed(title="🏎️ F1 Current Season Info", color=discord.Color.red())
            embed.add_field(name="Drivers (Top 10)", value=self._build_driver_embed(drivers) or "N/A", inline=False)
            embed.add_field(name="Constructors (Top 10)", value=self._build_constructor_embed(constructors) or "N/A", inline=False)
            
            if next_race:
                race_info = f"**{next_race['name']}**\n{next_race['circuit']}\n📅 {next_race['date']}"
                embed.add_field(name="Next Race (IST)", value=race_info, inline=False)
            
            await ctx.send(embed=embed)

    @commands.command(name="f1c")
    async def f1_circuit(self, ctx, *, search_term: str):
        async with ctx.typing():
            # Get current season circuits first (to prioritize active tracks like Albert Park over Adelaide for "Australia")
            current_circuits_data = self._fetch_data("circuits.json")
            circuits = []
            if current_circuits_data:
                circuits.extend(current_circuits_data['MRData']['CircuitTable']['Circuits'])
            
            # Find closest match
            search_query = search_term.lower()
            found_circuit = None
            
            # Helper function to find a circuit in a list
            def search_circuit_list(circuit_list):
                # Try exact matches first
                for circuit in circuit_list:
                    if search_query == circuit['circuitId'].lower() or search_query == circuit['Location']['country'].lower() or search_query == circuit['Location']['locality'].lower():
                        return circuit
                # Then partial matches
                for circuit in circuit_list:
                    if search_query in circuit['circuitId'].lower() or search_query in circuit['circuitName'].lower() or search_query in circuit['Location']['country'].lower() or search_query in circuit['Location']['locality'].lower():
                        return circuit
                return None
                
            found_circuit = search_circuit_list(circuits)
            
            # If not found in current calendar, search all historical circuits
            if not found_circuit:
                all_circuits_data = self._fetch_data("circuits.json?limit=1000") # using 1000 to get all historical
                if all_circuits_data:
                    all_circuits = all_circuits_data['MRData']['CircuitTable']['Circuits']
                    found_circuit = search_circuit_list(all_circuits)
                    
            if not found_circuit:
                await ctx.send(f"Could not find a circuit matching '{search_term}'.")
                return
                
            circuit_id = found_circuit['circuitId']
            
            # Now fetch the latest race results for this circuit
            # /circuits/<circuitId>/races.json gives all races at this circuit.
            races_data = self._fetch_data(f"circuits/{circuit_id}/races.json?limit=100")
            
            last_winner = "Unknown"
            last_year = "Unknown"
            
            if races_data and races_data['MRData']['RaceTable']['Races']:
                races = races_data['MRData']['RaceTable']['Races']
                # They are usually chronological, so the last one is the most recent
                last_race = races[-1]
                last_year = last_race['season']
                round_num = last_race['round']
                
                # Fetch results for that specific race to find the winner
                results_data = self._fetch_data(f"{last_year}/{round_num}/results.json")
                if results_data and results_data['MRData']['RaceTable']['Races']:
                    try:
                        winner = results_data['MRData']['RaceTable']['Races'][0]['Results'][0]['Driver']
                        last_winner = f"{winner['givenName']} {winner['familyName']}"
                    except (KeyError, IndexError):
                        pass

            embed = discord.Embed(title=f"🏎️ {found_circuit['circuitName']}", url=found_circuit.get('url', ''), color=discord.Color.red())
            
            info = f"**Location:** {found_circuit['Location']['locality']}, {found_circuit['Location']['country']}\n"
            info += f"**Previous Winner ({last_year}):** {last_winner}"
            
            embed.description = info
            
            image_url = self._get_circuit_image_url(circuit_id)
            embed.set_image(url=image_url)
            
            current_year = datetime.now().year
            embed.set_footer(text=f"Note: The displayed circuit layout may vary from current {current_year} FIA Formula 1 regulations")

            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(F1Command(bot))
