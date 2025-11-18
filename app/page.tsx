import { NavHeader } from '@/components/nav-header'
import { GameCard } from '@/components/game-card'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { TrendingUp, Star, DollarSign, Tag } from 'lucide-react'
import Link from 'next/link'

// Mock data
const topRatedGames = [
  { id: '1', name: 'The Last of Us Part II', coverImage: '/the-last-of-us-game-cover.jpg', averageRating: 9.5, currentPrice: 39.99, categories: ['Ação', 'Aventura'] },
  { id: '2', name: 'Red Dead Redemption 2', coverImage: '/red-dead-redemption-game-cover.jpg', averageRating: 9.3, currentPrice: 59.99, categories: ['Ação', 'RPG'] },
  { id: '3', name: 'God of War', coverImage: '/god-of-war-game-cover.jpg', averageRating: 9.2, currentPrice: 49.99, categories: ['Ação', 'Aventura'] },
  { id: '4', name: 'Elden Ring', coverImage: '/generic-fantasy-game-cover.png', averageRating: 9.4, currentPrice: 59.99, categories: ['RPG', 'Aventura'] },
  { id: '5', name: 'Baldurs Gate 3', coverImage: '/baldurs-gate-game-cover.jpg', averageRating: 9.6, currentPrice: 59.99, categories: ['RPG', 'Estratégia'] },
  { id: '6', name: 'Cyberpunk 2077', coverImage: '/cyberpunk-game-cover.png', averageRating: 8.5, currentPrice: 29.99, categories: ['RPG', 'Ação'] },
]

const bestPriceGames = [
  { id: '7', name: 'Hollow Knight', coverImage: '/hollow-knight-game-cover.jpg', averageRating: 9.0, currentPrice: 7.49, priceDown: true, categories: ['Plataforma', 'Indie'] },
  { id: '8', name: 'Hades', coverImage: '/hades-game-cover.png', averageRating: 9.1, currentPrice: 12.49, priceDown: true, categories: ['Roguelike', 'Ação'] },
  { id: '9', name: 'Stardew Valley', coverImage: '/stardew-valley-game-cover.png', averageRating: 9.3, currentPrice: 9.99, priceDown: true, categories: ['Simulação', 'Indie'] },
  { id: '10', name: 'Celeste', coverImage: '/celeste-game-cover.jpg', averageRating: 8.9, currentPrice: 4.99, priceDown: true, categories: ['Plataforma', 'Indie'] },
]

const mostWatchedGames = [
  { id: '11', name: 'GTA VI', coverImage: '/gta-6-game-cover.jpg', averageRating: 0, currentPrice: 69.99, categories: ['Ação', 'Aventura'] },
  { id: '12', name: 'Starfield', coverImage: '/starfield-game-cover.png', averageRating: 7.8, currentPrice: 69.99, categories: ['RPG', 'Ficção'] },
]

const featuredCategories = [
  { name: 'RPG', count: 1234, color: 'from-purple-500 to-pink-500' },
  { name: 'Ação', count: 2156, color: 'from-orange-500 to-red-500' },
  { name: 'Aventura', count: 1876, color: 'from-blue-500 to-cyan-500' },
  { name: 'Indie', count: 3421, color: 'from-green-500 to-emerald-500' },
]

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      <NavHeader />
      
      <main className="container mx-auto px-4 py-8 space-y-12">
        {/* Hero Section */}
        <section className="relative rounded-xl overflow-hidden bg-gradient-to-r from-primary/20 to-accent/20 p-8 md:p-12">
          <div className="relative z-10">
            <h1 className="text-4xl md:text-5xl font-bold mb-4 text-balance">
              Descubra, Avalie e Monitore seus Jogos Favoritos
            </h1>
            <p className="text-lg text-muted-foreground mb-6 max-w-2xl text-pretty">
              A plataforma definitiva para gamers que querem compartilhar opiniões e encontrar os melhores preços.
            </p>
            <div className="flex flex-wrap gap-3">
              <Link href="/games">
                <Button size="lg" className="font-semibold">
                  Explorar Jogos
                </Button>
              </Link>
              <Link href="/signup">
                <Button size="lg" variant="outline" className="font-semibold">
                  Criar Conta
                </Button>
              </Link>
            </div>
          </div>
        </section>

        {/* Top Rated Games */}
        <section>
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <TrendingUp className="h-6 w-6 text-primary" />
              <h2 className="text-2xl font-bold">Mais Bem Avaliados</h2>
            </div>
            <Link href="/games?sort=rating">
              <Button variant="ghost">Ver todos</Button>
            </Link>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            {topRatedGames.map((game) => (
              <GameCard key={game.id} {...game} />
            ))}
          </div>
        </section>

        {/* Best Prices Today */}
        <section>
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <DollarSign className="h-6 w-6 text-accent" />
              <h2 className="text-2xl font-bold">Melhores Preços Hoje</h2>
            </div>
            <Link href="/games?sort=price">
              <Button variant="ghost">Ver todos</Button>
            </Link>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {bestPriceGames.map((game) => (
              <GameCard key={game.id} {...game} />
            ))}
          </div>
        </section>

        {/* Most Watched */}
        <section>
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-2">
              <Star className="h-6 w-6 text-accent" />
              <h2 className="text-2xl font-bold">Mais Monitorados</h2>
            </div>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {mostWatchedGames.map((game) => (
              <GameCard key={game.id} {...game} />
            ))}
          </div>
        </section>

        {/* Featured Categories */}
        <section>
          <div className="flex items-center gap-2 mb-6">
            <Tag className="h-6 w-6 text-primary" />
            <h2 className="text-2xl font-bold">Categorias em Destaque</h2>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {featuredCategories.map((category) => (
              <Link key={category.name} href={`/categories/${category.name.toLowerCase()}`}>
                <Card className="group hover:ring-2 hover:ring-primary transition-all cursor-pointer">
                  <CardHeader>
                    <div className={`h-24 rounded-lg bg-gradient-to-br ${category.color} mb-4 group-hover:scale-105 transition-transform`} />
                    <CardTitle>{category.name}</CardTitle>
                    <CardDescription>{category.count} jogos</CardDescription>
                  </CardHeader>
                </Card>
              </Link>
            ))}
          </div>
        </section>
      </main>
    </div>
  )
}
