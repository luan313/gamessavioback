'use client'

import { NavHeader } from '@/components/nav-header'
import { GameCard } from '@/components/game-card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Slider } from '@/components/ui/slider'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Search, SlidersHorizontal } from 'lucide-react'
import { useState } from 'react'

// Mock data
const allGames = [
  { id: '1', name: 'The Last of Us Part II', coverImage: '/the-last-of-us-game-cover.jpg', averageRating: 9.5, currentPrice: 39.99, categories: ['Ação', 'Aventura'] },
  { id: '2', name: 'Red Dead Redemption 2', coverImage: '/red-dead-redemption-game-cover.jpg', averageRating: 9.3, currentPrice: 59.99, categories: ['Ação', 'RPG'] },
  { id: '3', name: 'God of War', coverImage: '/god-of-war-game-cover.jpg', averageRating: 9.2, currentPrice: 49.99, categories: ['Ação', 'Aventura'] },
  { id: '4', name: 'Elden Ring', coverImage: '/generic-fantasy-game-cover.png', averageRating: 9.4, currentPrice: 59.99, categories: ['RPG', 'Aventura'] },
  { id: '5', name: 'Baldurs Gate 3', coverImage: '/baldurs-gate-game-cover.jpg', averageRating: 9.6, currentPrice: 59.99, categories: ['RPG', 'Estratégia'] },
  { id: '6', name: 'Cyberpunk 2077', coverImage: '/cyberpunk-game-cover.png', averageRating: 8.5, currentPrice: 29.99, categories: ['RPG', 'Ação'] },
  { id: '7', name: 'Hollow Knight', coverImage: '/hollow-knight-game-cover.jpg', averageRating: 9.0, currentPrice: 7.49, priceDown: true, categories: ['Plataforma', 'Indie'] },
  { id: '8', name: 'Hades', coverImage: '/hades-game-cover.png', averageRating: 9.1, currentPrice: 12.49, priceDown: true, categories: ['Roguelike', 'Ação'] },
  { id: '9', name: 'Stardew Valley', coverImage: '/stardew-valley-game-cover.png', averageRating: 9.3, currentPrice: 9.99, priceDown: true, categories: ['Simulação', 'Indie'] },
  { id: '10', name: 'Celeste', coverImage: '/celeste-game-cover.jpg', averageRating: 8.9, currentPrice: 4.99, priceDown: true, categories: ['Plataforma', 'Indie'] },
  { id: '11', name: 'GTA VI', coverImage: '/gta-6-game-cover.jpg', averageRating: 8.0, currentPrice: 69.99, categories: ['Ação', 'Aventura'] },
  { id: '12', name: 'Starfield', coverImage: '/starfield-game-cover.png', averageRating: 7.8, currentPrice: 69.99, categories: ['RPG', 'Ficção'] },
]

export default function GamesPage() {
  const [searchQuery, setSearchQuery] = useState('')
  const [minRating, setMinRating] = useState([0])
  const [sortBy, setSortBy] = useState('popular')
  const [showFilters, setShowFilters] = useState(false)

  return (
    <div className="min-h-screen bg-background">
      <NavHeader />
      
      <main className="container mx-auto px-4 py-8">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold">Explorar Jogos</h1>
          <Button
            variant="outline"
            onClick={() => setShowFilters(!showFilters)}
            className="lg:hidden"
          >
            <SlidersHorizontal className="h-4 w-4 mr-2" />
            Filtros
          </Button>
        </div>

        <div className="flex gap-6">
          {/* Filters Sidebar */}
          <aside className={`${showFilters ? 'block' : 'hidden'} lg:block w-full lg:w-64 space-y-6`}>
            <Card>
              <CardHeader>
                <CardTitle className="text-lg">Filtros</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Search */}
                <div className="space-y-2">
                  <Label htmlFor="search">Buscar</Label>
                  <div className="relative">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                    <Input
                      id="search"
                      type="search"
                      placeholder="Nome do jogo..."
                      className="pl-10"
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                    />
                  </div>
                </div>

                {/* Category */}
                <div className="space-y-2">
                  <Label htmlFor="category">Categoria</Label>
                  <Select>
                    <SelectTrigger id="category">
                      <SelectValue placeholder="Todas as categorias" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">Todas</SelectItem>
                      <SelectItem value="action">Ação</SelectItem>
                      <SelectItem value="rpg">RPG</SelectItem>
                      <SelectItem value="adventure">Aventura</SelectItem>
                      <SelectItem value="indie">Indie</SelectItem>
                      <SelectItem value="strategy">Estratégia</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Rating */}
                <div className="space-y-2">
                  <Label>Nota Mínima: {minRating[0]}</Label>
                  <Slider
                    value={minRating}
                    onValueChange={setMinRating}
                    max={10}
                    step={0.5}
                    className="mt-2"
                  />
                </div>

                {/* Sort */}
                <div className="space-y-2">
                  <Label htmlFor="sort">Ordenar por</Label>
                  <Select value={sortBy} onValueChange={setSortBy}>
                    <SelectTrigger id="sort">
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

                <Button className="w-full" variant="outline">
                  Limpar filtros
                </Button>
              </CardContent>
            </Card>
          </aside>

          {/* Games Grid */}
          <div className="flex-1">
            <div className="mb-4 text-sm text-muted-foreground">
              Mostrando {allGames.length} jogos
            </div>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4">
              {allGames.map((game) => (
                <GameCard key={game.id} {...game} />
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
