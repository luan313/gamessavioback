import { NavHeader } from '@/components/nav-header'
import { GameCard } from '@/components/game-card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { ArrowLeft } from 'lucide-react'
import Link from 'next/link'

// Mock data
const categoryData = {
  name: 'RPG',
  slug: 'rpg',
  description: 'Role-Playing Games com histórias profundas e sistemas de progressão complexos',
  count: 1234,
}

const categoryGames = [
  { id: '2', name: 'Red Dead Redemption 2', coverImage: '/red-dead-redemption-game-cover.jpg', averageRating: 9.3, currentPrice: 59.99, categories: ['Ação', 'RPG'] },
  { id: '4', name: 'Elden Ring', coverImage: '/generic-fantasy-game-cover.png', averageRating: 9.4, currentPrice: 59.99, categories: ['RPG', 'Aventura'] },
  { id: '5', name: 'Baldurs Gate 3', coverImage: '/baldurs-gate-game-cover.jpg', averageRating: 9.6, currentPrice: 59.99, categories: ['RPG', 'Estratégia'] },
  { id: '6', name: 'Cyberpunk 2077', coverImage: '/cyberpunk-game-cover.png', averageRating: 8.5, currentPrice: 29.99, categories: ['RPG', 'Ação'] },
  { id: '12', name: 'Starfield', coverImage: '/starfield-game-cover.png', averageRating: 7.8, currentPrice: 69.99, categories: ['RPG', 'Ficção'] },
]

export default function CategoryDetailPage() {
  return (
    <div className="min-h-screen bg-background">
      <NavHeader />
      
      <main className="container mx-auto px-4 py-8">
        <Link href="/categories" className="inline-flex items-center text-sm text-muted-foreground hover:text-foreground mb-6 transition-colors">
          <ArrowLeft className="h-4 w-4 mr-1" />
          Voltar para categorias
        </Link>

        <div className="flex items-start justify-between mb-8">
          <div>
            <div className="flex items-center gap-3 mb-2">
              <h1 className="text-3xl font-bold">{categoryData.name}</h1>
              <Badge variant="secondary" className="text-base">
                {categoryData.count} jogos
              </Badge>
            </div>
            <p className="text-muted-foreground max-w-2xl">
              {categoryData.description}
            </p>
          </div>

          <Select defaultValue="popular">
            <SelectTrigger className="w-[180px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="popular">Mais populares</SelectItem>
              <SelectItem value="rating">Nota mais alta</SelectItem>
              <SelectItem value="price-low">Menor preço</SelectItem>
              <SelectItem value="price-high">Maior preço</SelectItem>
              <SelectItem value="recent">Mais recente</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
          {categoryGames.map((game) => (
            <GameCard key={game.id} {...game} />
          ))}
        </div>
      </main>
    </div>
  )
}
