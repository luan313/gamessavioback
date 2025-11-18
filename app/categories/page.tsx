import { NavHeader } from '@/components/nav-header'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Gamepad2 } from 'lucide-react'
import Link from 'next/link'

// Mock categories data
const categories = [
  { id: '1', name: 'RPG', slug: 'rpg', count: 1234, description: 'Role-Playing Games com histórias profundas', color: 'from-purple-500 to-pink-500' },
  { id: '2', name: 'Ação', slug: 'acao', count: 2156, description: 'Jogos de ação e combate', color: 'from-orange-500 to-red-500' },
  { id: '3', name: 'Aventura', slug: 'aventura', count: 1876, description: 'Explore mundos e resolva puzzles', color: 'from-blue-500 to-cyan-500' },
  { id: '4', name: 'Indie', slug: 'indie', count: 3421, description: 'Jogos independentes criativos', color: 'from-green-500 to-emerald-500' },
  { id: '5', name: 'Estratégia', slug: 'estrategia', count: 892, description: 'Planejamento tático e estratégico', color: 'from-yellow-500 to-orange-500' },
  { id: '6', name: 'Simulação', slug: 'simulacao', count: 654, description: 'Simule experiências realistas', color: 'from-teal-500 to-blue-500' },
  { id: '7', name: 'Plataforma', slug: 'plataforma', count: 743, description: 'Saltos e corridas precisas', color: 'from-pink-500 to-purple-500' },
  { id: '8', name: 'Roguelike', slug: 'roguelike', count: 456, description: 'Permadeath e procedural generation', color: 'from-red-500 to-orange-500' },
  { id: '9', name: 'Horror', slug: 'horror', count: 328, description: 'Experiências de terror e suspense', color: 'from-gray-700 to-gray-900' },
  { id: '10', name: 'Esportes', slug: 'esportes', count: 521, description: 'Jogos de esportes e competição', color: 'from-lime-500 to-green-500' },
  { id: '11', name: 'Corrida', slug: 'corrida', count: 412, description: 'Velocidade e competição', color: 'from-cyan-500 to-blue-500' },
  { id: '12', name: 'Puzzle', slug: 'puzzle', count: 789, description: 'Desafios de lógica e raciocínio', color: 'from-indigo-500 to-purple-500' },
]

export default function CategoriesPage() {
  return (
    <div className="min-h-screen bg-background">
      <NavHeader />
      
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Categorias</h1>
          <p className="text-muted-foreground">
            Explore jogos por gênero e estilo
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {categories.map((category) => (
            <Link key={category.id} href={`/categories/${category.slug}`}>
              <Card className="group hover:ring-2 hover:ring-primary transition-all cursor-pointer h-full">
                <CardHeader>
                  <div className={`h-32 rounded-lg bg-gradient-to-br ${category.color} mb-4 group-hover:scale-105 transition-transform flex items-center justify-center`}>
                    <Gamepad2 className="h-16 w-16 text-white/90" />
                  </div>
                  <CardTitle className="flex items-center justify-between">
                    {category.name}
                    <Badge variant="secondary">{category.count}</Badge>
                  </CardTitle>
                  <CardDescription>{category.description}</CardDescription>
                </CardHeader>
              </Card>
            </Link>
          ))}
        </div>
      </main>
    </div>
  )
}
